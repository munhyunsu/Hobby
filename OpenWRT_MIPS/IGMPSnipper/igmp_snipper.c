/*
 * tcpdump를 이용해서 igmp 패킷을 스니핑
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
//#include <sys/types.h>
#include <sys/wait.h>

int execute_program(char* argv[]);

int main(int argc, char* argv[])
{
    int return_value = 0; // 함수 실행 반환 변수 저장

    /* 인자 확인 */
    if (argc < 2) {
        printf("We need 1 argument\n");
        return -1;
    } // if (argv < 2)

    /* 인자 만들기 */
    int index;
    char** argv_subset = malloc((argc)*sizeof(char*));
    for(index = 0; index < (argc-1); index++) {
        argv_subset[index] = argv[index+1];
    }
    argv_subset[argc] = NULL;

    return_value = execute_program(argv_subset);
    printf("Executed program terminate, with %d\n\n", return_value);

    return 0;
} // int main(void)


int execute_program(char* argv[])
{
    pid_t my_pid; // pid 저장용
    int status = 0; // 차일드 프로세스 상태
    int timeout = 5; // 타임 아웃

    printf("%s %s %s\n", argv[0], argv[1], argv[2]);
    /* 차일드 프로세스 생성 및 실행 */
    my_pid = fork();
    if (my_pid == 0) { // 차일드 프로세스는 true
                       // 부모 프로세스는 false
        printf("child process(%d) execute %s\n", getpid(), argv[0]);
        if (execve(argv[0], (char **)argv, NULL) == -1) { // 프로세스
                                                          // 실패 가능성
            perror("child process execve failed"); // %m은 error code
            return -1;
        } // if (execve(argv[0], (char **)argv, NULL) == -1)
    } // if (my_pid == 0)

    /* 차일드 프로세스 대기 */
    printf("parent process(%d) wait for child process(%d)\n", 
            getpid(), my_pid);
    while (waitpid(my_pid, &status, WNOHANG) == 0) {
        timeout = timeout - 1;
        if (timeout < 0) {
            //system("reset");
            perror("timeout");
            kill(my_pid, SIGTERM);
            return -1;
        } else {
            sleep(1);
        } // else
    } // while (waitpid(my_pid, %status, WNOHANG) == 0)

    /* 차일드 프로세스 정보 출력 
     * 차일드 프로세스가 비정상 종료되었을 때 처리 */
    printf("%s WEXITSTATUS %d WIFEXITED %d [status %d]\n",
            argv[0], WEXITSTATUS(status), WIFEXITED(status), status);
    if (WEXITSTATUS(status) != 0 || WIFEXITED(status) != 1) {
        perror("%s failed");
        return -1;
    } // if (WEXITSTATUS(status) != 0 || WIFEXITED(status) != 1)

    return 0;
} // int exec_program
