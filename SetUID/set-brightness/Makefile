CC      := gcc
CFLAGS  := -O2 -Wall
TARGET  := set-brightness
SRC     := set-brightness.c
PREFIX  := /usr/local/bin

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $<

install: $(TARGET)
	@echo "Installing $(TARGET) to $(PREFIX)..."
	sudo cp $(TARGET) $(PREFIX)/
	sudo chown root:root $(PREFIX)/$(TARGET)
	sudo chmod 4755 $(PREFIX)/$(TARGET)
	@echo "Installed with setuid root."

uninstall:
	@echo "Removing $(PREFIX)/$(TARGET)..."
	sudo rm -f $(PREFIX)/$(TARGET)

clean:
	rm -f $(TARGET)

