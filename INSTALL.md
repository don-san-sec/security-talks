# Building from source
## 1. Pull code from the repository
```bash
git clone https://github.com/don-san-sec
```
## 2. Make hooks executable
```bash
chmod +x .githooks/*
```
## 3. Set hooks directory
```bash
git config core.hookspath .githooks
```
## 4. Run `pre-commit` hook manually or commit changes
```bash
./.githooks/pre-commit
```
