require('dotenv').config();
const express = require('express');
const cors = require('cors');
const OpenAI = require('openai');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

const dbPath = path.resolve(__dirname, '../../back/db.sqlite3');

app.use(cors({origin: 'http://localhost:5173'}));
app.use(express.json());

app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;

        // 사용자의 의도를 파악
        const intentCheck = await openai.chat.completions.create({
            model: 'gpt-3.5-turbo',
            messages: [
                {
                    role: 'system',
                    content: `당신은 'MoFin이'라는 이름의 귀엽고 똑똑한 금융 상담사입니다. 
사용자의 메시지를 분석하여 금융상품 추천이 필요한지 판단해주세요.
다음과 같은 경우 추천이 필요하다고 판단하세요:
- 상품 추천을 직접적으로 요청하는 경우
- 예금/적금 가입에 대해 문의하는 경우
- 금리나 수익률에 대해 문의하는 경우
응답은 "YES" 또는 "NO"로만 해주세요.`
                },
                {
                    role: 'user',
                    content: message
                }
            ],
            temperature: 0.1,
            max_tokens: 10
        });

        const needsRecommendation = intentCheck.choices[0].message.content.trim().toUpperCase() === 'YES';

        if (!needsRecommendation) {
            // 일반적인 응대
            const generalResponse = await openai.chat.completions.create({
                model: 'gpt-3.5-turbo',
                messages: [
                    {
                        role: 'system',
                        content: `당신은 'MoFin'라는 이름의 귀엽고 똑똑한 금융 상담사입니다. 
다음과 같은 특징을 가지고 대화해주세요:

1. 성격과 말투:
- 친근하고 상냥한 말투를 사용하되, 전문성은 유지합니다
- 가끔 웃는 이모지를 사용합니다
- 존댓말을 사용하되, 딱딱하지 않게 대화합니다

2. 응답 스타일:
- "MoFin이 알려드릴게요!", "MoFin이 도와드릴게요~" 같은 표현을 사용합니다
- 복잡한 금융 용어는 쉽게 풀어서 설명합니다
- 따뜻하고 공감하는 태도를 보입니다

하지만 주의할 점:
- 귀여운 캐릭터이지만, 금융 전문가로서의 신뢰성은 잃지 않습니다
- 이모지는 적절히 사용하되 과하지 않게 합니다
- 구체적인 금융상품 추천은 하지 않습니다`
                    },
                    {
                        role: 'user',
                        content: message
                    }
                ],
                temperature: 0.7,
                max_tokens: 500
            });

            return res.json({ message: generalResponse.choices[0].message.content });
        }

        // 금융상품 추천이 필요한 경우
        const db = new sqlite3.Database(dbPath);
        const query = `
            SELECT 
                d.kor_co_nm as bank_name,
                d.fin_prdt_nm as product_name,
                ROUND(o.intr_rate, 2) as base_rate,
                ROUND(o.intr_rate2, 2) as prime_rate,
                o.save_trm as term
            FROM savings_depositproducts d
            LEFT JOIN savings_depositoptions o 
            ON d.fin_prdt_cd = o.fin_prdt_cd
            ORDER BY o.intr_rate2 DESC
            LIMIT 10
        `;

        db.all(query, [], async (err, products) => {
            if (err) {
                console.error('DB 오류:', err);
                db.close();
                return res.status(500).json({ error: err.message });
            }

            const completion = await openai.chat.completions.create({
                model: 'gpt-3.5-turbo',
                messages: [
                    {
                        role: 'system',
                        content: `당신은 'MoFin'라는 이름의 귀엽고 똑똑한 금융 상담사입니다. 
금융상품을 추천할 때는 다음과 같은 스타일로 설명해주세요:

1. 시작 멘트:
- "MoFin이 찾아본 최고의 상품을 소개해드릴게요! ✨"
- "고객님께 딱 맞는 상품을 골라봤어요! "

2. 설명 포함 사항:
- 상품명과 은행명
- 기본금리와 우대금리 (이해하기 쉽게 설명)
- 가입기간과 주요 특징
- 추천 이유

3. 설명 스타일:
- 쉽고 친근한 말투 사용
- 복잡한 금융 용어는 풀어서 설명
- 적절한 이모지 사용 (💰, ✨, 📈)
- 고객의 입장에서 이해하기 쉽게 정리

4. 마무리:
- "다른 궁금하신 점 있으시다면 MoFin에게 언제든 물어보세요!"
- "더 자세한 상담이 필요하시다면 말씀해주세요~"

주의사항:
- 전문성과 신뢰성은 유지하면서 친근하게 설명하기
- 이모지는 적절히 사용 (과하지 않게)
- 정확한 수치와 정보 전달에 집중`
                    },
                    {
                        role: 'user',
                        content: `현재 상품 목록: ${JSON.stringify(products)}\n\n문의사항: ${message}`
                    }
                ],
                temperature: 0.7,
                max_tokens: 500
            });

            db.close();
            res.json({ message: completion.choices[0].message.content });
        });
    } catch (error) {
        console.error('오류:', error);
        res.json({ 
            message: "앗, MoFin이 잠시 실수를 했어요! 🥺 다시 한 번 말씀해 주시겠어요? 더 맛있게 답변해드릴게요!" 
        });
    }
});

app.listen(3000, () => console.log('맛있는 MoFin이 서버 실행 중!'));