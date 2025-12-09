---
description: AzureへGit連携でデプロイする方法
---

このガイドでは、現在開発中のアプリケーション（FastAPIバックエンド + Next.jsフロントエンド）を、GitHub経由でMicrosoft Azure（Azure App Service / Static Web Apps）にデプロイする手順を説明します。

## 前提条件
1. **GitHubアカウント**と**リポジトリ**が作成されていること。
2. **Microsoft Azureアカウント**を持っていること。
3. ローカルのコードがGitHubリポジトリにプッシュされていること。

---

## ステップ1: 構成ファイルの準備

デプロイ時にAzureが起動コマンドを正しく認識できるように、設定を確認します。

### 1-1. バックエンド (FastAPI)
`backend/` ディレクトリに、起動コマンドを指定する `startup.sh` (Linux用) または `requirements.txt` が正しく配置されているか確認します。
Azure App Service for Pythonは自動的に `requirements.txt` を検知しますが、起動コマンドを明示的に指定することをお勧めします。

**backend/startup.sh** (作成が必要な場合)
```bash
#!/bin/bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```
※ `gunicorn` を使用する場合、`requirements.txt` に `gunicorn` を追加してください。

### 1-2. フロントエンド (Next.js)
`apps/customer/package.json` の `build` スクリプトが正しく動作することを確認します。

---

## ステップ2: Azure リソースの作成

Azure Portal (https://portal.azure.com) にログインしてリソースを作成します。

### 2-1. バックエンド用 (Azure Web App for Python)
1. 「リソースの作成」から **"Web App"** を検索して選択します。
2. **基本設定**:
   - **サブスクリプション**: お使いのサブスクリプション
   - **リソースグループ**: 新規作成 (例: `rg-zoff-scope`)
   - **名前**: 一意の名前 (例: `app-zoff-backend`)
   - **公開**: `Code`
   - **ランタイムスタック**: `Python 3.11` (お使いのバージョンに合わせて)
   - **OS**: `Linux`
   - **地域**: `Japan East`
3. 「確認と作成」→「作成」をクリック。

### 2-2. フロントエンド用 (Azure Static Web Apps)
Next.jsのデプロイには **Azure Static Web Apps** が最適です。
1. 「リソースの作成」から **"Static Web App"** を検索して選択します。
2. **基本設定**:
   - **リソースグループ**: 先ほどと同じものを選択
   - **名前**: 一意の名前 (例: `stapp-zoff-frontend`)
   - **プランの種類**: `Free` (開発用ならFreeで十分です)
   - **地域**: `East Asia` (Static Web Appsはグローバル分散なので近場を選択)
   - **デプロイの詳細**: "GitHub" を選択し、アカウントを連携します。
   - **組織/リポジトリ/ブランチ**: 対象のリポジトリとブランチ(`main`など)を選択。
   - **ビルドの詳細**:
     - **ビルドのプリセット**: `Next.js`
     - **App location**: `/apps/customer` (Next.jsアプリの場所)
     - **Api location**: (空欄でOK、またはPythonを使うなら設定)
     - **Output location**: (空欄でOK、自動検知されます)
3. 「確認と作成」をクリックすると、自動的にGitHub Actionsのワークフローファイルがリポジトリに追加され、デプロイが始まります。

---

## ステップ3: バックエンドのデプロイ設定 (GitHub Actions)

Web App (バックエンド) のデプロイ設定を行います。

1. Azure Portalで作成したバックエンドのWeb App (`app-zoff-backend`) を開きます。
2. 左メニューの **「デプロイメント センター」** を選択します。
3. **設定**:
   - **ソース**: `GitHub`
   - **組織/リポジトリ/ブランチ**: 対象を選択
4. 保存すると、GitHub Actionsのワークフローが自動生成されますが、**モノレポ構成（サブディレクトリにアプリがある）** ため、生成されたファイルを修正する必要があります。

### ワークフローファイルの修正
GitHubのリポジトリに `.github/workflows/` というフォルダができ、新しいYAMLファイルが追加されています。これを編集します。

以下のように、`working-directory` やパスを修正して `backend` ディレクトリのみを対象にします。

```yaml
# 例: backendディレクトリを対象にする設定
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pushd backend
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          popd
          
      - name: Zip artifact for deployment
        run: |
          pushd backend
          zip -r release.zip ./*
          popd
          
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: python-app
          path: backend/release.zip

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v3
        with:
          name: python-app

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: 'app-zoff-backend' # あなたのアプリ名
          package: '.'
          startup-command: 'uvicorn app.main:app --host 0.0.0.0 --port 8000' # または startup.sh
```

---

## ステップ4: 環境変数の設定

BackendとFrontendがつながるようにURL環境変数を設定します。

### バックエンド側 (CORS設定)
Azure PortalのWeb App > **「CORS」** 設定で、フロントエンドのURL (Static Web AppのURL) を許可リストに追加します。

### フロントエンド側 (API接続先)
Static Web Appの設定 > **「環境変数」** で、バックエンドのAPI URLを設定します。
- `NEXT_PUBLIC_API_URL`: `https://app-zoff-backend.azurewebsites.net` (あなたのバックエンドURL)

コード内で `fetch('http://127.0.0.1:8000/...')` となっている箇所は、この環境変数を使うように修正する必要があります。

例:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
fetch(`${API_BASE_URL}/staffs/`)
```
