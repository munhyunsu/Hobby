helloworld: helloworld.o
	$(CC) $(LDFLAGS) helloworld.o -o helloworld
helloworld.o: helloworld.c
	$(CC) $(LDFLAGS) -c helloworld.c

clean:
	rm *.o helloworld
