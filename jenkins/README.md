# Jenkins Integration

## Option 1: Create job manually (recommended)

1. Jenkins → **Manage Jenkins** → **Plugins**
2. Install plugins from `jenkins/plugins.txt`
3. **New Item** → `VavniServices-Playwright` → **Pipeline**
4. Pipeline settings:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/kunalpipaliya1/VavniServices.git`
   - Branch: `*/main`
   - Script Path: `Jenkinsfile`
5. Save and click **Build with Parameters**

## Option 2: Create job with Job DSL

1. Install **Job DSL** plugin
2. Create a **Freestyle** or **Pipeline** seed job
3. Add build step **Process Job DSLs**
4. Use DSL script: `jenkins/job.dsl`
5. Run the seed job once to create `VavniServices-Playwright`

## Schedule

Configured in `Jenkinsfile`:

| Trigger | Schedule |
|---|---|
| Daily run | `H 9 * * *` |
| Git poll | every 15 minutes |

## Parameters

| Name | Default | Description |
|---|---|---|
| `BASE_URL` | `http://localhost:3001` | App URL for login/register tests |
| `BROWSER` | `chromium` | Playwright browser |

## Reports

After each build Jenkins publishes:

- **Allure HTML Report** (`reports/html/allure-report/index.html`)
- **JUnit** results (`reports/junit/results.xml`)
- Archived artifacts from `reports/`

## Local test (same as Jenkins)

Windows:

```bat
jenkins\run-local.bat
```

Linux/macOS:

```bash
bash jenkins/run-local.sh
```

## GitHub webhook (optional)

1. Jenkins → job → **Configure** → **Build Triggers**
2. Enable **GitHub hook trigger for GITScm polling**
3. GitHub repo → **Settings** → **Webhooks**
4. Payload URL: `https://YOUR-JENKINS-URL/github-webhook/`

Then each push to `main` can trigger a build.
