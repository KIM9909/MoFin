require('dotenv').config();
const express = require('express');
const cors = require('cors');
const OpenAI = require('openai');

// 환경변수 로딩 확인을 위한 상세 로그
console.log('Current working directory:', process.cwd());
console.log('Environment variables:', {
    OPENAI_API_KEY: process.env.OPENAI_API_KEY ? 'Exists' : 'Not found'
});

// API 키가 없으면 종료
if (!process.env.OPENAI_API_KEY) {
    console.error('OPENAI_API_KEY is not set in .env file');
    process.exit(1);
}

const app = express();

// CORS 설정
app.use(cors({
    origin: 'http://localhost:5173', // Vue 개발 서버 주소
    methods: ['GET', 'POST'],
    credentials: true
}));
app.use(express.json());

// OpenAI 클라이언트 초기화
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

// 테스트용 라우트
app.get('/test', (req, res) => {
    res.json({ message: 'Server is running!' });
});

// 채팅 라우트
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        
        // OpenAI API 호출
        const completion = await openai.chat.completions.create({
            model: 'gpt-3.5-turbo',
            messages: [{ role: 'user', content: message }]
        });

        res.json({ message: completion.choices[0].message.content });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: '서버 오류가 발생했습니다.' });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});