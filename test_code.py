import unittest
from agents.agent import create_agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = create_agent()

    def test_agent_response_weather(self):
        query = "오늘 서울의 날씨는 어때?"
        response = self.agent.invoke(query)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_agent_response_ai(self):
        query = "최근 인공지능 기술에 대해 알려줘."
        response = self.agent.invoke(query)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

if __name__ == '__main__':
    unittest.main()