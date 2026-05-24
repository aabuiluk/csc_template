# Оновити форк з шаблоном

```bash
git config merge.ours.driver true
git remote add upstream https://github.com/ВИКЛАДАЧ/csc_template.git   # один раз
bash scripts/sync_from_template.sh
git push
```

`students/**` при merge не перезаписується (`.gitattributes`).
