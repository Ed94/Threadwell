Local credentials. Gitignored except this file.

| File | Contents |
| --- | --- |
| `twitter_cookies.txt` | Netscape cookies for gallery-dl |
| `credentials.toml` | `[catbox] userhash`, `[backup] id` and `root` |

Shape of `credentials.toml`:

```toml
[catbox]
userhash = ""

[backup]
id = "cozy"
root = ""
```

The scripts read these files. They never print the values.

Do not commit this folder. Do not paste the contents into chat or issues.
