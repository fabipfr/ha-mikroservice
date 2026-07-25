import unittest

import main


class RootResponseTests(unittest.TestCase):
    def test_root_returns_rendered_html(self) -> None:
        response = main.read_root()

        self.assertIn("<h1>Installation</h1>", response)
        self.assertIn("<code>", response)


if __name__ == "__main__":
    unittest.main()
