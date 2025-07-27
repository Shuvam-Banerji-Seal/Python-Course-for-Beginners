
import requests
import json

# Author: Niket Basu

class OpenTDBAPI:
    def __init__(self):
        self.base_url = "https://opentdb.com/api.php"

    def get_categories(self):
        """Fetches the list of available quiz categories."""
        url = "https://opentdb.com/api_category.php"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()['trivia_categories']
        except requests.exceptions.RequestException as e:
            print(f"Error fetching categories: {e}")
            return None

    def get_questions(self, num_questions, category=None, difficulty=None, quiz_type=None):
        """Fetches quiz questions based on the specified parameters."""
        params = {
            'amount': num_questions,
        }
        if category:
            params['category'] = category
        if difficulty:
            params['difficulty'] = difficulty
        if quiz_type:
            params['type'] = quiz_type

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if data['response_code'] == 0:
                return data['results']
            else:
                return []  # No questions found
        except requests.exceptions.RequestException as e:
            print(f"Error fetching questions: {e}")
            return None

