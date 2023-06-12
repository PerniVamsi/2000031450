
def __init__(self, port):
    self.port = port


def get_numbers(self, urls):
    numbers = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            numbers.extend(json.loads(response.content)["numbers"])

    numbers = sorted(set(numbers))
    return numbers

