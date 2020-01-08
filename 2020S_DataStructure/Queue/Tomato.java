import java.util.*;
import java.io.*;
 
// https://www.acmicpc.net/problem/7576
 
class Tomato {
    static int N;
    static int M;
    static int[][] box;
    static int[] dx = {1, -1, 0, 0};
    static int[] dy = {0, 0, 1, -1};
 
    static class Dot {
        int x;
        int y;
        int day;
 
        public Dot(int x, int y, int day) {
            this.x = x;
            this.y = y;
            this.day = day;
        }
    }
 
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        N = Integer.parseInt(st.nextToken());
        M = Integer.parseInt(st.nextToken());
 
        box = new int[M][N];
 
        for(int i=0; i<M; i++) {
            st = new StringTokenizer(br.readLine());
 
            for(int j=0; j<N; j++) {
                box[i][j] = Integer.parseInt(st.nextToken());
            }
        }
 
        bfs();
    }
 
    static void bfs() {
        Queue<Dot> q = new LinkedList<Dot>();
        int day = 0;
 
        // 토마토가 있는 좌표 찾아서 Queue에 넣기
        for(int i=0; i<M; i++) {
            for(int j=0; j<N; j++) {
                if(box[i][j] == 1) 
                    q.offer(new Dot(i, j, 0));
            }
        }
 
        // bfs 시작
        while(!q.isEmpty()) {
            Dot dot = q.poll();
            day = dot.day;
 
            for(int i=0; i<4; i++) {
                int nx = dot.x + dx[i];
                int ny = dot.y + dy[i];
 
                if(0 <= nx && nx < M && 0 <= ny && ny < N) {
                    if(box[nx][ny] == 0) {
                        box[nx][ny] = 1;
                        q.add(new Dot(nx, ny, day+1));
                    }
                }
            }
        }
 
        // 토마토가 다 익었는지 확인
        if(checkTomato())
            System.out.println(day);
        else
            System.out.println(-1);
    }    
 
    // box 배열에 0이 남아있다면 false, 아니면 true
    static boolean checkTomato() {
        for(int i=0; i<M; i++) {
            for(int j=0; j<N; j++) {
                if(box[i][j] == 0)
                    return false;
            }
        }
 
        return true;
    }
}
