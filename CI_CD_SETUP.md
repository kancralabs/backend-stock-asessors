# CI/CD Setup Guide

Panduan untuk setup CI/CD dengan GitHub Actions, Codecov, dan CodeRabbit.

## 1. GitHub Actions Setup

GitHub Actions sudah dikonfigurasi di [.github/workflows/ci.yml](.github/workflows/ci.yml).

Pipeline akan otomatis berjalan setiap:
- Push ke branch `main` atau `develop`
- Pull request ke branch `main` atau `develop`

### Jobs yang berjalan:
1. **Test & Coverage** - Run tests dengan minimum 80% coverage
2. **Lint** - Check formatting dan linting
3. **Build** - Build Docker image

## 2. Codecov Setup

### Step 1: Sign up ke Codecov
1. Pergi ke [codecov.io](https://codecov.io)
2. Login dengan GitHub account
3. Authorize Codecov untuk mengakses repository

### Step 2: Get Codecov Token
1. Pilih repository di Codecov dashboard
2. Copy `CODECOV_TOKEN` dari Settings

### Step 3: Add Secret ke GitHub
1. Pergi ke repository GitHub
2. Settings → Secrets and variables → Actions
3. Klik "New repository secret"
4. Name: `CODECOV_TOKEN`
5. Value: paste token dari Codecov
6. Klik "Add secret"

### Step 4: Add Badge ke README (Optional)
```markdown
[![codecov](https://codecov.io/gh/USERNAME/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/REPO)
```

## 3. CodeRabbit Setup

### Step 1: Install CodeRabbit
1. Pergi ke [GitHub Marketplace - CodeRabbit](https://github.com/marketplace/coderabbitai)
2. Klik "Install it for free"
3. Pilih repository yang ingin di-review
4. Authorize CodeRabbit

### Step 2: Configure CodeRabbit
File konfigurasi sudah ada di [.coderabbit.yaml](.coderabbit.yaml)

CodeRabbit akan otomatis:
- Review setiap Pull Request
- Memberikan feedback dalam Bahasa Indonesia
- Check untuk security vulnerabilities
- Suggest improvements

### Features CodeRabbit:
- Auto-reply di PR comments
- Security vulnerability detection
- Code quality suggestions
- Performance recommendations

## 4. Verify Setup

### Test CI/CD Pipeline:
1. Create a new branch
```bash
git checkout -b test/ci-cd
```

2. Make a small change
```bash
echo "# Test" >> test.txt
git add test.txt
git commit -m "test: verify CI/CD"
git push origin test/ci-cd
```

3. Create Pull Request di GitHub

4. Check:
   - ✅ GitHub Actions running
   - ✅ Tests passing
   - ✅ Coverage uploaded to Codecov
   - ✅ CodeRabbit reviewing PR

## 5. Troubleshooting

### GitHub Actions failing?
- Check logs di Actions tab
- Pastikan PostgreSQL dan Redis services running
- Verify environment variables

### Codecov not uploading?
- Check `CODECOV_TOKEN` ada di GitHub Secrets
- Verify coverage.xml file generated
- Check Codecov Action logs

### CodeRabbit not reviewing?
- Check CodeRabbit installed di repository
- Verify `.coderabbit.yaml` configuration
- Try re-running the review dengan comment: `@coderabbitai review`

## 6. Badges for README

Tambahkan badges ini ke README.md:

```markdown
![CI/CD](https://github.com/USERNAME/REPO/workflows/CI%2FCD%20Pipeline/badge.svg)
[![codecov](https://codecov.io/gh/USERNAME/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/USERNAME/REPO)
[![CodeRabbit](https://img.shields.io/badge/AI--Review-CodeRabbit-blue)](https://coderabbit.ai)
```

Ganti `USERNAME` dan `REPO` dengan GitHub username dan repository name.

## 7. Best Practices

### Coverage:
- Maintain minimum 80% coverage
- Write tests untuk semua features baru
- Test edge cases

### Commits:
- Use conventional commits (feat:, fix:, docs:, etc)
- Keep commits small dan focused
- Write descriptive commit messages

### Pull Requests:
- Fill PR template lengkap
- Add screenshots jika ada perubahan UI
- Wait untuk CI/CD pass sebelum merge
- Address CodeRabbit feedback

## Need Help?

Open an issue atau hubungi maintainers.
