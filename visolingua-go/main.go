package main

import (
	"embed"
	"io/fs"
	"log"
	"os"
	"path/filepath"

	"github.com/wailsapp/wails/v2"
	"github.com/wailsapp/wails/v2/pkg/options"
	"github.com/wailsapp/wails/v2/pkg/options/assetserver"
	"github.com/wailsapp/wails/v2/pkg/options/windows"
	"github.com/wailsapp/wails/v2/pkg/logger"
)

//go:embed frontend/dist
var assets embed.FS

func main() {
	// Setup logging to file
	logPath := filepath.Join(os.TempDir(), "visolingua-go.log")
	logFile, err := os.OpenFile(logPath, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err == nil {
		log.SetOutput(logFile)
		defer logFile.Close()
	} else {
		// If logging fails, try stderr
		log.SetOutput(os.Stderr)
	}

	log.Println("=== VisoLingua Go Starting ===")
	log.Println("Log file:", logPath)
	log.Printf("Working directory: %s", getCurrentDir())

	// Check embedded assets
	entries, err := assets.ReadDir("frontend/dist")
	if err != nil {
		log.Printf("ERROR: Failed to read embedded assets: %v", err)
		log.Fatal(err)
	}
	log.Printf("Found %d embedded files:", len(entries))
	for _, entry := range entries {
		log.Printf("  - %s", entry.Name())
	}

	// Create application instance
	app := NewApp()
	if app == nil {
		log.Fatal("Failed to create app instance")
	}
	log.Println("App instance created")

	// Create application options
	log.Println("Creating Wails app...")

	// Create sub-filesystem pointing to frontend/dist
	distFS, err := fs.Sub(assets, "frontend/dist")
	if err != nil {
		log.Fatalf("Failed to create sub-filesystem: %v", err)
	}

	err = wails.Run(&options.App{
		Title:  "VisoLingua",
		Width:  600,
		Height: 500,
		AssetServer: &assetserver.Options{
			Assets: distFS,
		},
		BackgroundColour: &options.RGBA{R: 0, G: 0, B: 0, A: 0},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
		},
		Logger:          logger.NewDefaultLogger(),
		AlwaysOnTop:     true,
		Frameless:       false,
		Windows: &windows.Options{
			WebviewIsTransparent: true,
			WindowIsTranslucent:  true,
		},
	})

	if err != nil {
		log.Printf("ERROR: %v\n", err)
		log.Fatal(err)
	}

	log.Println("App exited normally")
}

func getCurrentDir() string {
	dir, _ := os.Getwd()
	return dir
}