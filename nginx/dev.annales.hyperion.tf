server {
    listen 80;
    server_name dev.annales.hyperion.tf;
    client_max_body_size 20M;
    keepalive_timeout 0;

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:6094;
    }
}