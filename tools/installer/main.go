package main

import (
	"archive/zip"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

const (
	repoZipURL = "https://github.com/sl5net/SL5-aura-service/archive/refs/heads/main.zip"
	appName    = "sl5-aura-service"
)

func ensureTerminal() {
	if runtime.GOOS == "windows" {
		return
	}
	if os.Getenv("AURA_INSIDE_TERMINAL") == "1" {
		return
	}

	fi, err := os.Stdin.Stat()
	if err == nil && (fi.Mode()&os.ModeCharDevice) != 0 {
		return
	}

	execPath, err := os.Executable()
	if err != nil {
		return
	}

	terminals := [][]string{
		{"konsole", "-e"},
		{"gnome-terminal", "--"},
		{"x-terminal-emulator", "-e"},
		{"xterm", "-e"},
		{"alacritty", "-e"},
		{"kitty"},
	}

	for _, term := range terminals {
		if path, err := exec.LookPath(term[0]); err == nil {
			args := append(term[1:], execPath)
			cmd := exec.Command(path, args...)
			cmd.Env = append(os.Environ(), "AURA_INSIDE_TERMINAL=1")
			if err := cmd.Start(); err == nil {
				os.Exit(0)
			}
		}
	}
}

func getInstallDir() (string, error) {
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}

	if runtime.GOOS == "windows" {
		localAppData := os.Getenv("LOCALAPPDATA")
		if localAppData != "" {
			return filepath.Join(localAppData, appName), nil
		}
		return filepath.Join(homeDir, "AppData", "Local", appName), nil
	}

	xdgData := os.Getenv("XDG_DATA_HOME")
	if xdgData != "" {
		return filepath.Join(xdgData, appName), nil
	}
	return filepath.Join(homeDir, ".local", "share", appName), nil
}

func downloadFile(url, destPath string) error {
	resp, err := http.Get(url)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected HTTP status: %s", resp.Status)
	}

	out, err := os.Create(destPath)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	return err
}

func unzipArchive(srcZip, destDir string) error {
	r, err := zip.OpenReader(srcZip)
	if err != nil {
		return err
	}
	defer r.Close()

	if err := os.MkdirAll(destDir, 0755); err != nil {
		return err
	}

	for _, f := range r.File {
		parts := strings.Split(f.Name, "/")
		if len(parts) <= 1 {
			continue
		}
		relPath := strings.Join(parts[1:], string(filepath.Separator))
		if relPath == "" {
			continue
		}

		targetPath := filepath.Join(destDir, relPath)

		if f.FileInfo().IsDir() {
			if err := os.MkdirAll(targetPath, f.Mode()); err != nil {
				return err
			}
			continue
		}

		if err := os.MkdirAll(filepath.Dir(targetPath), 0755); err != nil {
			return err
		}

		outFile, err := os.OpenFile(targetPath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
		if err != nil {
			return err
		}

		rc, err := f.Open()
		if err != nil {
			outFile.Close()
			return err
		}

		_, err = io.Copy(outFile, rc)
		rc.Close()
		outFile.Close()
		if err != nil {
			return err
		}
	}
	return nil
}

func runSetup(installDir string) error {
	var cmd *exec.Cmd

	switch runtime.GOOS {
		case "windows":
			batPath := filepath.Join(installDir, "setup", "windows11_setup.bat")
			cmd = exec.Command("cmd.exe", "/c", batPath)
		case "darwin", "linux":
			shPath := filepath.Join(installDir, "setup", "linux_mac_setup.sh")
			if err := os.Chmod(shPath, 0755); err != nil {
				return err
			}
			cmd = exec.Command("/bin/bash", shPath)
		default:
			return fmt.Errorf("unsupported OS: %s", runtime.GOOS)
	}

	cmd.Dir = installDir
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	return cmd.Run()
}

func main() {
	ensureTerminal()

	fmt.Println("============================================")
	fmt.Println("   SL5 Aura Service - 1-Click Bootstrap     ")
	fmt.Println("============================================")

	targetDir, err := getInstallDir()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error detecting target path: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("[1/3] Destination: %s\n", targetDir)

	tmpZip := filepath.Join(os.TempDir(), "sl5-aura-main.zip")
	defer os.Remove(tmpZip)

	fmt.Println("[2/3] Downloading repository archive...")
	if err := downloadFile(repoZipURL, tmpZip); err != nil {
		fmt.Fprintf(os.Stderr, "Download failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("[2/3] Extracting files...")
	if err := unzipArchive(tmpZip, targetDir); err != nil {
		fmt.Fprintf(os.Stderr, "Extraction failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("[3/3] Starting setup...")
	if err := runSetup(targetDir); err != nil {
		fmt.Fprintf(os.Stderr, "Setup failed: %v\n", err)
		os.Exit(1)
	}

	fmt.Println("Installation completed.")
}
