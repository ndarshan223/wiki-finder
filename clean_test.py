#!/usr/bin/env python3

# Test text cleaning
test_text = "GitLab | CI/CD | Pipeline\\nSetup"
cleaned = test_text.replace('|', '').replace('\\\\', '').replace('\\n', ' ').strip()
print(f"Original: {repr(test_text)}")
print(f"Cleaned:  {repr(cleaned)}")