package main

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

// This is a minimal starter template for a Go/Gin API
// You can use Windsurf to expand this into a full application

func main() {
	// Initialize the Gin router
	r := gin.Default()

	// Define a simple health check endpoint
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "healthy",
		})
	})

	// Start the server
	log.Println("Starting server on :8080")
	r.Run(":8080")
}
