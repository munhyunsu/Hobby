/**
 * @file process_monitor.c
 * @Author LuHa(munhyunsu@gmail.com)
 * 참고: http://bewareofgeek.livejournal.com/2945.html
 * @Version 0.0.1
 */

#include <sys/socket.h>
#include <linux/netlink.h>
#include <linux/connector.h>
#include <linux/cn_proc.h>
#include <signal.h>
#include <errno.h>
#include <stdbool.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/*
 * connect to netlink
 * returns netlink socket, or -1 on error
 */
/**넷링크 소켓 연결
 * PROC 이벤트를 받는 넷링크 소켓을 반환
 */
static int nl_connect()
{
    int rc;
    /**넷링크 소켓
     * 소켓 생성 반환값을 저장
     */
    int nl_sock;
    /**넷링크 클라이언트 주소
     * sockaddr_nl안에 여러 자료가 있음
     * http://man7.org/linux/man-pages/man7/netlink.7.html
     * struct sockaddr_nl {
     * sa_family_t     nl_family;
     * unsigned short  nl_pad;
     * pid_t           nl_pid;
     * __u32           nl_groups;
     * };
     */
    struct sockaddr_nl sa_nl;

    /**소켓 생성
     * PF_NETLINK: Protocol Family Netlink
     * SOCK_DGRAM: Socket Datagram
     * NETLINK_CONNECTOR: Netlink connector 형식의 소켓
     * 
     * 표준 지정이 안 되어있기 때문에
     * SOCK_DGRAM은 모든 Linux OS에서 지원하리라는 보장이 안 됨
     * (대부분 지원이 되기는 함)
     * SOCK_RAW는 레드햇에서 지원된다고 알려져있음
     */
    nl_sock = socket(PF_NETLINK, SOCK_DGRAM, NETLINK_CONNECTOR);
    if (nl_sock == -1) {
        perror("socket");
        return -1;
    }

    /**주소 패밀리 지정
     * 넷링크 주소 형태
     */
    sa_nl.nl_family = AF_NETLINK;
    /** 넷링크 그룹 지정
     * http://lxr.free-electrons.com
     *     /source/include/uapi/linux/connector.h#L30
     * 프로세스 이벤트 커넥터
     * 여기서 지정한 Netlink 그룹에 합류함
     * 그룹간에는 Multicast가 오고갈 수 있음
     * CN_IDX_PROC을 지정해서 PROC 이벤트 멀티캐스트를 인식
     */
    sa_nl.nl_groups = CN_IDX_PROC;
    /**넷링크 유니캐스트 주소 지정
     * 커널이 목적지일 경우 0
     * 아닐 경우 소켓을 가지고 있는 프로세스의 PID
     * 우리는 커널로 메시지를 보내는 것이 아니므로 프로세스 PID
     */
    sa_nl.nl_pid = getpid();

    /**생성한 소켓 바인드
     * sa_nl에 바인드
     * 만일 오류가 날 경우 종료
     */
    rc = bind(nl_sock, (struct sockaddr *)&sa_nl, sizeof(sa_nl));
    if (rc == -1) {
        perror("bind");
        close(nl_sock);
        return -1;
    }

    /**연결된 소켓 반환
     * 생성, 바인드까지 된 소켓 반환
     */
    return nl_sock;
}

/*
 * subscribe on proc events (process notifications)
 */
/**PROC 이벤트 탐지
 * CN_IDX_PROC 그룹으로 전송되는 메시지 인식
 */
static int set_proc_ev_listen(int nl_sock, bool enable)
{
    int rc;
    /**넷링크 커넥터 메시지 구조체
     * 넷링크 커넥터 메시지
     * packing 관련: http://stackoverflow.com/
     *                   questions/4306186/structure-padding-and-packing
     * 커넥터 관련: http://lxr.free-electrons.com/
     *                  source/include/uapi/linux/cn_proc.h#L27
     * NLMSG_ALIGNTO: 4U
     * 4로 끝나는 주소에 데이터 저장
     */
    struct __attribute__ ((aligned(NLMSG_ALIGNTO))) {
        /**넷링크 헤더*/
        struct nlmsghdr nl_hdr;
        /**커넥터 메시지*/
        struct __attribute__ ((__packed__)) {
            struct cn_msg cn_msg;
            /**PROC 멀티캐스트 오퍼레이터
             * PROC_CN_MCAST_LISTEN = 1
             * PROC_CN_MCAST_IGNORE = 2
             */
            enum proc_cn_mcast_op cn_mcast;
        };
    } nlcn_msg;

    /**전송할 패킷 제작
     * 참고: http://man7.org/linux/man-pages/man7/netlink.7.html
     *       https://www.kernel.org/doc/Documentation/
     *           connector/connector.txt
     * struct nlmsghdr {
     *     __u32 nlmsg_len;
     *     __u16 nlmsg_type;
     *     __u16 nlmsg_flags;
     *     __u32 nlmsg_seq;
     *     __u32 nlmsg_pid;
     * }
     * struct cn_msg {
     *     struct cb_id id;
     *     __u32        seq;
     *     __u32        ack;
     *     __u32        len;
     *     __u8         data[0];
     * }
     * struct cb_id {
     *     __u32        idx;
     *     __u32        val;
     * }
     * 1. 메모리 할당
     * 2. 패킷 길이 조립
     * 3. 패킷 전송 포트(PID) 조립
     * 4. 메시지 타입 조립: NLMSG_DONE 메시지 완료
     * 5. 커넥터 메시지 아이디 조립: Inter data exchange, value
     * 6. 커넥터 메시지 길이: proc_cn_mcast_op 길이
     * 7. 멀티캐스트 가입 or 탈퇴
     */
    memset(&nlcn_msg, 0, sizeof(nlcn_msg));
    nlcn_msg.nl_hdr.nlmsg_len = sizeof(nlcn_msg);
    nlcn_msg.nl_hdr.nlmsg_pid = getpid();
    nlcn_msg.nl_hdr.nlmsg_type = NLMSG_DONE;

    nlcn_msg.cn_msg.id.idx = CN_IDX_PROC;
    nlcn_msg.cn_msg.id.val = CN_VAL_PROC;
    nlcn_msg.cn_msg.len = sizeof(enum proc_cn_mcast_op);

    nlcn_msg.cn_mcast = 
            enable ? PROC_CN_MCAST_LISTEN : PROC_CN_MCAST_IGNORE;

    /**조립한 패킷 전송
     * 멀티캐스트로 전송
     */
    rc = send(nl_sock, &nlcn_msg, sizeof(nlcn_msg), 0);
    if (rc == -1) {
        perror("netlink send");
        return -1;
    }

    return 0;
}

/**PID를 이용해 프로세스 이름 가져오기
 * /proc/PID/cmdline 데이터를 가져온다
 */
const char* get_process_name_by_pid(const int pid)
{
    /** 프로세스 이름이 저장될 메모리 할당 */
    char* name = (char*) calloc(1024, sizeof(char));
    if (name != NULL) {
        sprintf(name, "/proc/%d/cmdline", pid);
        FILE* f = fopen(name,"r");
        if (f != NULL) {
            /** 파일을 읽어옴 */
            size_t size;
            size = fread(name, sizeof(char), 1024, f);
            if (size > 0) {
                if ('\n' == name[size-1]) {
                    name[size-1] = '\0';
                }
            }
            fclose(f);
        }
    }
    return name;
}



/*
 * handle a single process event
 */
/** 보기좋은 종료를 위한 전역 변수 */
static volatile bool need_exit = false;
/**PROC 이벤트 처리 함수
 * 소켓에 도착한 PROC 멀티캐스트 이벤트를 처리
 * 입력: 넷링크 소켓
 */
static int handle_proc_ev(int nl_sock)
{
    /** 받은 데이터 양 저장 변수 */
    int rc;
    /**넷링크 커넥터 메시지 구조체
     * 넷링크 커넥터 메시지
     * packing 관련: http://stackoverflow.com/
     *                   questions/4306186/structure-padding-and-packing
     * 커넥터 관련: http://lxr.free-electrons.com/
     *                  source/include/uapi/linux/cn_proc.h#L27
     * NLMSG_ALIGNTO: 4U
     * 4로 끝나는 주소에 데이터 저장
     */
    struct __attribute__ ((aligned(NLMSG_ALIGNTO))) {
        struct nlmsghdr nl_hdr;
        struct __attribute__ ((__packed__)) {
            struct cn_msg cn_msg;
            struct proc_event proc_ev;
        };
    } nlcn_msg;

    /**이벤트 처리
     * 프로세스가 종료되거나 컴퓨터가 종료될 때 까지 지속
     */
    while (!need_exit) {
        /**소켓에서 메시지 받기
         * 메시지 길이가 -1이 나올 경우 에러
         */
        rc = recv(nl_sock, &nlcn_msg, sizeof(nlcn_msg), 0);
        if (rc == 0) {
            /* shutdown? */
            return 0;
        } else if (rc == -1) {
            /**에러 종류 체크
             * 만일 인터럽트로 인한 에러일 경우 계속 진행
             */
            if (errno == EINTR) continue;
            perror("netlink recv");
            return -1;
        }
        /**PROC Event 메시지 처리
         * 참고: http://lxr.free-electrons.com/
         *           source/include/uapi/linux/cn_proc.h#L27
         * PROC_EVENT_NONE = 0x00000000
         * PROC_EVENT_FORK = 0x00000001
         * PROC_EVENT_EXEC = 0x00000002
         * PROC_EVENT_UID  = 0x00000004
         * PROC_EVENT_GID  = 0x00000040
         * PROC_EVENT_SID  = 0x00000080
         * PROC_EVENT_PTRACE = 0x00000100
         * PROC_EVENT_COMM = 0x00000200
         * PROC_EVENT_COREDUMP = 0x40000000
         * PROC_EVENT_EXIT = 0x80000000
         *
         */
        switch (nlcn_msg.proc_ev.what) {
            /** 아무 이벤트가 아닐 때 */
            case PROC_EVENT_NONE:
                printf("0x%08x, %lld, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.ack.err
                        );
                break;
            /** fork() 호출 */
            case PROC_EVENT_FORK:
                printf("0x%08x, %lld, %u, %u, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.fork.parent_pid,
                        nlcn_msg.proc_ev.event_data.fork.parent_tgid,
                        nlcn_msg.proc_ev.event_data.fork.child_pid,
                        nlcn_msg.proc_ev.event_data.fork.child_tgid
                        );
                break;
            /** exec() 호출 */
            case PROC_EVENT_EXEC:
                printf("0x%08x, %lld, %u, %u, %s\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.exec.process_pid,
                        nlcn_msg.proc_ev.event_data.exec.process_tgid,
                        get_process_name_by_pid(
                            nlcn_msg.proc_ev.event_data.exec.process_pid)
                        );
                break;
            /** UID 변경 */
            case PROC_EVENT_UID:
                printf("0x%08x, %lld, %u, %u, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.id.process_pid,
                        nlcn_msg.proc_ev.event_data.id.process_tgid,
                        nlcn_msg.proc_ev.event_data.id.r.ruid,
                        nlcn_msg.proc_ev.event_data.id.e.euid
                        );
                break;
            /** GID 변경 */
            case PROC_EVENT_GID:
                printf("0x%08x, %lld, %u, %u, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.id.process_pid,
                        nlcn_msg.proc_ev.event_data.id.process_tgid,
                        nlcn_msg.proc_ev.event_data.id.r.rgid,
                        nlcn_msg.proc_ev.event_data.id.e.egid
                        );
                break;
            /** SID 변경 */
            case PROC_EVENT_SID:
                printf("0x%08x, %lld, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.sid.process_pid,
                        nlcn_msg.proc_ev.event_data.sid.process_tgid
                        );
                break;
            case PROC_EVENT_PTRACE:
                printf("0x%08x, %lld, %u, %u, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.ptrace.process_pid,
                        nlcn_msg.proc_ev.event_data.ptrace.process_tgid,
                        nlcn_msg.proc_ev.event_data.ptrace.tracer_pid,
                        nlcn_msg.proc_ev.event_data.ptrace.tracer_tgid
                        );
                break;
            case PROC_EVENT_COMM:
                printf("0x%08x, %lld, %u, %u, %s\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.comm.process_pid,
                        nlcn_msg.proc_ev.event_data.comm.process_tgid,
                        nlcn_msg.proc_ev.event_data.comm.comm
                        );
                break;
            case PROC_EVENT_COREDUMP:
                printf("0x%08x, %lld, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.coredump.process_pid,
                        nlcn_msg.proc_ev.event_data.coredump.process_tgid
                        );
                break;
            case PROC_EVENT_EXIT:
                printf("0x%08x, %lld, %u, %u, %u, %u\n",
                        nlcn_msg.proc_ev.what,
                        nlcn_msg.proc_ev.timestamp_ns,
                        nlcn_msg.proc_ev.event_data.exit.process_pid,
                        nlcn_msg.proc_ev.event_data.exit.process_tgid,
                        nlcn_msg.proc_ev.event_data.exit.exit_code,
                        nlcn_msg.proc_ev.event_data.exit.exit_signal
                        );
                break;
            default:
                printf("unhandled proc event\n");
                break;
        }
    }

    return 0;
}


/**SIGINT 핸들러
 * 끝내야함을 알림
 */
static void on_sigint(int unused)
{
    printf("user send signal: %d\n", unused);
    need_exit = true;
}

/**프로그램 이쁘게 종료
 * 넷 소켓 및 이벤트 핸들러 닫기
 */
static void close_exit(int nl_sock, int rc)
{
    close(nl_sock);
    exit(rc);
}

/**\brief 프로세스 모니터 메인
 *
 * N Socket을 이용해서 시그널을 받아 처리
 */
int main(int argc, const char *argv[])
{
    /**변수 생성
     * NETLINK_CONNECTOR 변수 생성
     * return value 생성
     */
    int nl_sock;
    int rc = EXIT_SUCCESS;

    /**인터럽트 관리
     * SIGINT 핸들러 지정
     * SIGINT를 처리하는 동안 다른 인터럽트가 발생할 수 있음
     * 따라서 인터럽트 enable
     */
    signal(SIGINT, on_sigint);
    siginterrupt(SIGINT, true);

    /**넷링크 소켓 생성
     * nl_connect() 호출
     * 생성 실패시 프로그램 종료
     */
    nl_sock = nl_connect();
    if (nl_sock == -1)
        exit(EXIT_FAILURE);

    /**PROC 멀티캐스트 그룹에 가입
     * CN_IDX_PROC 그룹에 가입 메시지 전송
     */
    rc = set_proc_ev_listen(nl_sock, true);
    if (rc == -1) {
        rc = EXIT_FAILURE;
        //goto out;
        close_exit(nl_sock, rc);
    }

    /**PROC 멀티캐스트 메시지 처리
     * CN_IDX_PROC 그룹에서 발생한 메시지 처리
     */
    rc = handle_proc_ev(nl_sock);
    if (rc == -1) {
        rc = EXIT_FAILURE;
        //goto out;
        close_exit(nl_sock, rc);
    }

    /**PROC 멀티캐스트 그룹에서 탈퇴
     * 무언가 잘못 되었을 경우 탈퇴하고 종료
     * 그런데 여기까지 올 수 있을까?
     * 죽은 코드인 것 같으나 일단 유지
     */
	set_proc_ev_listen(nl_sock, false);

//out:
//    close(nl_sock);
//    exit(rc);
}
