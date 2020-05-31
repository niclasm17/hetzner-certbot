# Certbot Hetzner DNS Challenge (for Docker)

If you're using certbot with Docker, you may face the problem, that the [shell script provided by Hetzner](https://community.hetzner.com/tutorials/letsencrypt-dns) does not work with the official `certbot/certbot` [image](https://hub.docker.com/r/certbot/certbot/).

Thankfully, the certbot container ships with python3 and the neccessery modules, which make it possible to write own python auth and cleanup scripts.

## Usage

- Save the files somewhere on your server, i.e: `/home/user/certbot/hetzner`
- Edit the `hetzner-auth-token` file and paste your DNS auth token there
- Run `docker` command
- (Optional) configure `crontab` to run the script automatically

```
docker run --rm --name certbot -v /home/user/certbot/hetzner:/hetzner certbot/certbot certonly --manual --preferred-challenges=dns --manual-auth-hook "python /hetzner/certbot-hetzner-auth.py" --manual-cleanup-hook "python /hetzner/certbot-hetzner-cleanup.py" -d '<domain.tld>' -d '*.<domain.tld>'
```
