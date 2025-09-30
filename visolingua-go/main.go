package main

import (
	"embed"
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
	}

	log.Println("=== VisoLingua Go Starting ===")
	log.Println("Log file:", logPath)

	// Create application instance
	app := NewApp()
	if app == nil {
		log.Fatal("Failed to create app instance")
	}
	log.Println("App instance created")

	// Create application options
	log.Println("Creating Wails app...")
	err = wails.Run(&options.App{
		Title:  "VisoLingua",
		Width:  600,
		Height: 500,
		AssetServer: &assetserver.Options{
			Assets: assets,
		},
		BackgroundColour: &options.RGBA{R: 26, G: 26, B: 26, A: 255},
		OnStartup:        app.startup,
		Bind: []interface{}{
			app,
		},
		Logger: logger.NewDefaultLogger(),
		Windows: &windows.Options{
			WebviewIsTransparent: false,
			WindowIsTranslucent:  false,
		},
	})

	if err != nil {
		log.Printf("ERROR: %v\n", err)
		log.Fatal(err)
	}

	log.Println("App exited normally")
}