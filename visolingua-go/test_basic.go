// +build ignore

package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"
)

func main() {
	logPath := filepath.Join(os.TempDir(), "visolingua-go-test.log")
	f, _ := os.Create(logPath)
	defer f.Close()

	fmt.Fprintf(f, "Test started at %v\n", time.Now())
	fmt.Fprintf(f, "Temp dir: %s\n", os.TempDir())
	fmt.Fprintf(f, "Working dir: %s\n", os.Getenv("PWD"))

	fmt.Printf("Test log written to: %s\n", logPath)
	time.Sleep(3 * time.Second)
}
