#include <stdio.h>
#include <time.h>

void get_current_time(char* time_string, size_t max_size) {
    time_t current_time = time(NULL);
    struct tm* timeinfo = localtime(&current_time);
    strftime(time_string, max_size, "%Y-%m-%d %H:%M:%S", timeinfo);
}

int main() {
    char time_string[20];
    get_current_time(time_string, sizeof(time_string));
    printf("%s\n", time_string);
    return 0;
}
