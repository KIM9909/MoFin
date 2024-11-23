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

        // 먼저 사용자의 의도를 파악
        const intentCheck = await openai.chat.completions.create({
            model: 'gpt-3.5-turbo',
            messages: [
                {
                    role: 'system',
                    content: `당신은 금융상품 전문 상담사입니다. 
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
                        content: `당신은 친절한 금융상품 전문 상담사입니다. 
고객의 문의사항에 대해 전문적이고 친절하게 응대해주세요.
단, 구체적인 금융상품 추천은 하지 말아주세요.`
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
                        content: `당신은 금융상품 전문 상담사입니다.
고객 응대 시 다음을 포함해 설명해주세요:
- 추천 상품명과 은행명
- 기본금리와 우대금리
- 가입기간과 주요 특징
- 추천 이유
`
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
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => console.log('서버 실행중'));