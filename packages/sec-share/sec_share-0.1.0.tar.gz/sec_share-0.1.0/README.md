# SecureShare

A command-line tool for securely sharing code snippets with automatic secret detection and redaction.

## Installation

```bash
pip install share-secure
```

## Usage

```bash
# Share a file
sec-share -t "My Code" -l python my_script.py

# Share from stdin
cat my_script.py | sec-share -t "My Code" -l python
```

## Features

- Automatic detection and redaction of sensitive information
- Support for multiple programming languages
- Secure sharing with expiration dates
- Easy-to-use command-line interface

## Environment Variables

Before using SecureShare, set the following environment variables:

```bash
export VITE_SUPABASE_URL="your-supabase-url"
export VITE_SUPABASE_ANON_KEY="your-supabase-anon-key"
```

## License

MIT License
