// +build windows

package main

import (
	"fmt"
	"syscall"
	"unsafe"
)

var (
	user32               = syscall.NewLazyDLL("user32.dll")
	procMessageBoxW      = user32.NewProc("MessageBoxW")
)

func showErrorDialog(title, message string) {
	titlePtr, _ := syscall.UTF16PtrFromString(title)
	messagePtr, _ := syscall.UTF16PtrFromString(message)
	procMessageBoxW.Call(
		0,
		uintptr(unsafe.Pointer(messagePtr)),
		uintptr(unsafe.Pointer(titlePtr)),
		0x10, // MB_ICONERROR
	)
}

func init() {
	// Catch panics and show dialog
	defer func() {
		if r := recover(); r != nil {
			showErrorDialog("VisoLingua Error", fmt.Sprintf("Application crashed: %v\n\nCheck log at: %%TEMP%%\\visolingua-go.log", r))
		}
	}()
}
