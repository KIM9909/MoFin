from locust import HttpUser, task, between
import logging
from datetime import datetime
import random
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_unique_username():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    random_string = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"test_{timestamp}_{random_string}"

class BankUser(HttpUser):
    host = "http://127.0.0.1:8000/"
    wait_time = between(1, 3)
    token = None
    username = None
    password = "testpass123!@#"
    
    def on_start(self):
        """테스트 시작 시 회원가입 수행"""
        try:
            self.username = generate_unique_username()
            
            signup_data = {
                "username": self.username,
                "email": f"{self.username}@example.com",
                "password1": self.password,
                "password2": self.password,
                "nickname": f"닉네임_{self.username[-8:]}",
                "birth": "1990-01-01",
                "preference": "저축",
                "annual_income": 5000,
                "total_assets": 10000
            }
            
            signup_response = self.client.post(
                "accounts/signup/",
                data=signup_data,
                name="/accounts/signup/"
            )
            logger.info(f"Signup response: {signup_response.status_code}")
            
            if signup_response.status_code == 201:
                response_data = signup_response.json()
                self.token = response_data.get('key', '')
                if self.token:
                    logger.info("Successfully got token from signup")
                else:
                    logger.error("No token in signup response")
            
        except Exception as e:
            logger.error(f"Error in on_start: {str(e)}")
    
    def get_headers(self):
        if self.token:
            return {
                'Authorization': f'Token {self.token}'
            }
        return {}

    # Savings & Products Tasks
    @task(3)
    def get_deposit_products(self):
        """예금 상품 목록 조회"""
        try:
            response = self.client.get(
                "savings/deposit_products/",
                name="/savings/deposit_products/"
            )
            logger.info(f"Deposit products response: {response.status_code}")
        except Exception as e:
            logger.error(f"Error in get_deposit_products: {str(e)}")
    
    @task(3)
    def get_savings_products(self):
        """적금 상품 목록 조회"""
        try:
            response = self.client.get(
                "savings/savings_products/",
                name="/savings/savings_products/"
            )
            logger.info(f"Savings products response: {response.status_code}")
        except Exception as e:
            logger.error(f"Error in get_savings_products: {str(e)}")

    # Recommendations Tasks
    @task(2)
    def get_recommendations(self):
        """추천 상품 조회"""
        if self.token:
            try:
                response = self.client.get(
                    "recommendations/get-recommendations/",
                    headers=self.get_headers(),
                    name="/recommendations/get-recommendations/"
                )
                logger.info(f"Recommendations response: {response.status_code}")
            except Exception as e:
                logger.error(f"Error in get_recommendations: {str(e)}")

    @task(2)
    def get_finance_status(self):
        """재무 상태 조회"""
        if self.token:
            try:
                response = self.client.get(
                    "recommendations/finance-status/",
                    headers=self.get_headers(),
                    name="/recommendations/finance-status/"
                )
                logger.info(f"Finance status response: {response.status_code}")
            except Exception as e:
                logger.error(f"Error in get_finance_status: {str(e)}")

    # User Account Tasks
    @task(2)
    def get_user_info(self):
        """사용자 정보 조회"""
        if self.token:
            try:
                response = self.client.get(
                    "accounts/user/",
                    headers=self.get_headers(),
                    name="/accounts/user/"
                )
                logger.info(f"User info response: {response.status_code}")
            except Exception as e:
                logger.error(f"Error in get_user_info: {str(e)}")


    @task(1)
    def change_password(self):
        """비밀번호 변경"""
        if self.token:
            try:
                # CSRF 토큰 획득
                csrf_response = self.client.get("admin/")
                csrf_token = csrf_response.cookies.get('csrftoken')
                
                if csrf_token:
                    headers = {
                        **self.get_headers(),
                        'X-CSRFToken': csrf_token,
                    }
                    
                    new_password = f"new{self.password}"
                    password_data = {
                        "old_password": self.password,
                        "new_password1": new_password,
                        "new_password2": new_password
                    }
                    
                    response = self.client.post(
                        "accounts/password/change/",
                        json=password_data,
                        headers=headers,
                        cookies={'csrftoken': csrf_token},
                        name="/accounts/password/change/"
                    )
                    logger.info(f"Password change response: {response.status_code}")
                    
                    if response.status_code == 200:
                        self.password = new_password
            except Exception as e:
                logger.error(f"Error in change_password: {str(e)}")

    @task(1)
    def test_logout_flow(self):
        """로그아웃 후 새 계정 생성"""
        if self.token:
            try:
                # CSRF 토큰 획득
                csrf_response = self.client.get("admin/")
                csrf_token = csrf_response.cookies.get('csrftoken')
                
                if csrf_token:
                    headers = {
                        **self.get_headers(),
                        'X-CSRFToken': csrf_token,
                    }
                    
                    logout_response = self.client.post(
                        "accounts/logout/",
                        headers=headers,
                        cookies={'csrftoken': csrf_token},
                        name="/accounts/logout/"
                    )
                    logger.info(f"Logout response: {logout_response.status_code}")
                    
                    if logout_response.status_code == 200:
                        self.token = None
                        logger.info("Successfully logged out")
                        
                        # 새 계정 생성
                        self.username = generate_unique_username()
                        signup_data = {
                            "username": self.username,
                            "email": f"{self.username}@example.com",
                            "password1": self.password,
                            "password2": self.password,
                            "nickname": f"닉네임_{self.username[-8:]}",
                            "birth": "1990-01-01",
                            "preference": "저축",
                            "annual_income": 5000,
                            "total_assets": 10000
                        }
                        
                        signup_response = self.client.post(
                            "accounts/signup/",
                            data=signup_data,
                            name="/accounts/signup/"
                        )
                        
                        if signup_response.status_code == 201:
                            response_data = signup_response.json()
                            self.token = response_data.get('key', '')
                            logger.info("Successfully created new account after logout")
                    
            except Exception as e:
                logger.error(f"Error in test_logout_flow: {str(e)}")