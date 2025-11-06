#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>

void exploit(const char* target, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        return;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    
    if (inet_pton(AF_INET, target, &server_addr.sin_addr) <= 0) {
        close(sock);
        return;
    }

    struct timeval timeout = {5, 0};
    setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, &timeout, sizeof(timeout));
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        close(sock);
        return;
    }

    close(sock);
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        printf("用法: %s <目标IP> <端口> <访问间隔(秒)>\n", argv[0]);
        return 1;
    }

    const char* target = argv[1];
    int port = atoi(argv[2]);
    int interval = atoi(argv[3]);

    printf("开始无限访问 %s:%d（间隔%d秒），按 Ctrl+C 停止...\n", target, port, interval);

    while (1) {  // 无限循环，永不退出
        exploit(target, port);
        sleep(interval);
    }

    return 0;
}