$root = Split-Path -Parent $PSScriptRoot
$site = Join-Path $root "site"
$config = Join-Path $PSScriptRoot "quartz.config.yaml"

if (-not (Test-Path -LiteralPath (Join-Path $site ".git"))) {
  git clone --branch v5 --single-branch https://github.com/jackyzha0/quartz.git $site
}

Copy-Item -LiteralPath $config -Destination (Join-Path $site "quartz.config.yaml") -Force
Set-Location -LiteralPath $site
npm ci
npx quartz plugin install --from-config
npm install @quartz-themes/shimmering-focus
