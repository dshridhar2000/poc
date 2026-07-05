package main

import (
	"archive/zip"
	"os"
	"path/filepath"
)

func unzip(zipFile string) {

	r, _ := zip.OpenReader(zipFile)
	defer r.Close()

	for _, f := range r.File {

		path := filepath.Join("/tmp/uploads", f.Name)

		out, _ := os.Create(path)

		rc, _ := f.Open()

		defer rc.Close()
		defer out.Close()
	}
}
