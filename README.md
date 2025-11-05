# 🌍 EarthPulse

<div align="center">

![EarthPulse Banner](https://img.shields.io/badge/EarthPulse-Cloud%20Storage-blueviolet?style=for-the-badge)
![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**Your files, reimagined in the cloud** ☁️✨

A modern, beautiful cloud storage solution with a stunning glassmorphism UI, built with cutting-edge technologies.

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 📸 Preview

Experience a revolutionary cloud storage interface with:
- 🎨 **Stunning Glassmorphism Design** - Modern, translucent UI elements
- 🌈 **Animated Gradients** - Dynamic, eye-catching color transitions
- 🎭 **Smooth Animations** - Fluid interactions and transitions
- 📱 **Responsive Design** - Perfect on desktop, tablet, and mobile

---

## ✨ Features

### 🎯 Core Functionality
- **📤 File Upload** - Drag & drop or click to upload files (up to 200MB)
- **📥 File Download** - Fast and reliable file downloads
- **✏️ File Rename** - Easily rename your files with a beautiful modal
- **🗑️ File Delete** - Remove files with confirmation
- **🔍 File Search** - Quick search through your files

### 🎨 Design Features
- **Glassmorphism UI** - Modern glass-effect cards and components
- **Animated Gradients** - Living, breathing interface elements
- **3D Hover Effects** - Interactive depth on hover
- **Floating Animations** - Ambient background decorations
- **Responsive Layout** - Optimized for all screen sizes

### 🔧 Technical Features
- **Object Storage** - MinIO for efficient file storage
- **Metadata Database** - MongoDB for file information
- **REST API** - FastAPI backend with automatic documentation
- **Real-time Updates** - Instant UI updates after operations
- **Docker Support** - Easy deployment with Docker Compose

---

## 🚀 Quick Start

### Prerequisites

Make sure you have installed:
- [Docker](https://www.docker.com/get-started) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/earthpulse.git
   cd earthpulse
   ```

2. **Start the application**
   ```bash
   docker-compose up -d --build
   ```

3. **Access the application**
   - 🌐 **Frontend**: http://localhost:5173
   - 🔌 **API Docs**: http://localhost:8000/docs
   - 📦 **MinIO Console**: http://localhost:9001

That's it! The application is now running. 🎉

---

## 🏗️ Architecture

### Tech Stack

#### Frontend
- **SvelteKit** - Fast, modern JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Next-generation frontend tooling

#### Backend
- **FastAPI** - Modern, fast Python web framework
- **MongoDB** - Document-oriented NoSQL database
- **MinIO** - High-performance object storage
- **Uvicorn** - Lightning-fast ASGI server

#### Infrastructure
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container orchestration

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                              │
│                    (SvelteKit + Vite)                        │
│                     Port: 5173                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP/REST API
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                         Backend                              │
│                      (FastAPI)                               │
│                     Port: 8000                               │
└────────────┬────────────────────────┬────────────────────────┘
             │                        │
             │                        │
             ▼                        ▼
┌──────────────────────┐  ┌──────────────────────────┐
│      MongoDB         │  │        MinIO             │
│   (Metadata DB)      │  │   (Object Storage)       │
│    Port: 27017       │  │   Ports: 9000, 9001      │
└──────────────────────┘  └──────────────────────────┘
```

### Project Structure

```
EarthPulse/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main application entry
│   │   ├── models.py       # Data models
│   │   ├── database.py     # Database connection
│   │   └── storage.py      # MinIO storage client
│   └── requirements.txt    # Python dependencies
├── frontend/               # SvelteKit frontend
│   ├── src/
│   │   ├── routes/        # Page routes
│   │   ├── lib/           # Shared components
│   │   │   ├── components/
│   │   │   └── stores/    # State management
│   │   ├── app.css        # Global styles
│   │   └── app.html       # HTML template
│   └── package.json       # Node dependencies
├── data/                  # Persistent data
│   ├── mongo/            # MongoDB data
│   └── minio/            # MinIO data
├── docker-compose.yml    # Service orchestration
├── Dockerfile.backend    # Backend container
├── Dockerfile.frontend   # Frontend container
└── README.md            # This file
```

---

## 📚 API Documentation

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/files` | List all files (with optional search) |
| `POST` | `/files/upload` | Upload a new file |
| `GET` | `/files/{file_id}/download` | Download a file |
| `PUT` | `/files/{file_id}` | Rename a file |
| `DELETE` | `/files/{file_id}` | Delete a file |
| `GET` | `/health` | Health check endpoint |

### Interactive API Documentation

FastAPI provides interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎨 Design System

### Color Palette

```css
Primary Gradient:   #667eea → #764ba2 → #f093fb → #4facfe → #00f2fe
Purple:             #8b5cf6
Pink:               #ec4899
Blue:               #3b82f6
```

### Key Design Elements

- **Glassmorphism**: `backdrop-blur-xl` with transparent backgrounds
- **Gradients**: Animated multi-color gradients on buttons and backgrounds
- **Animations**: Float, gradient-shift, pulse-glow, and slide-up
- **Shadows**: Layered shadows for depth (shadow-xl, shadow-2xl)

---

## 🛠️ Development

### Running in Development Mode

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
MONGO_URL=mongodb://localhost:27017/filesdb
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=files
MINIO_SECURE=false
```

---

## 🐳 Docker Commands

### Essential Commands

```bash
# Start all services
docker-compose up -d

# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View running containers
docker-compose ps
```

### Individual Service Management

```bash
# Restart frontend only
docker-compose restart frontend

# View backend logs
docker-compose logs backend

# Execute command in backend container
docker-compose exec backend bash
```

---

## 📊 Database Schema

### File Document (MongoDB)

```json
{
  "_id": "ObjectId",
  "name": "example.pdf",
  "size": 1024000,
  "content_type": "application/pdf",
  "upload_date": "2025-11-03T10:00:00Z",
  "minio_object_id": "unique-object-identifier"
}
```

---

## 🔐 Security Considerations

- File size limit: 200MB (configurable)
- File type validation on upload
- Secure file storage with MinIO
- CORS enabled for development (configure for production)
- No authentication (add for production use)

---

## 🚀 Deployment

### Production Recommendations

1. **Add Authentication**: Implement user authentication and authorization
2. **Enable HTTPS**: Use SSL/TLS certificates
3. **Configure CORS**: Restrict allowed origins
4. **Set Resource Limits**: Configure Docker resource constraints
5. **Backup Strategy**: Implement regular backups for MongoDB and MinIO
6. **Environment Variables**: Use secrets management
7. **Monitoring**: Add logging and monitoring tools
8. **CDN**: Consider using a CDN for static assets

### Docker Compose Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [SvelteKit](https://kit.svelte.dev/) - Amazing frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [MinIO](https://min.io/) - High-performance object storage
- [MongoDB](https://www.mongodb.com/) - Flexible NoSQL database
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

<div align="center">

**Made with and ☕**

⭐ Star this repo if you find it helpful!

</div>
