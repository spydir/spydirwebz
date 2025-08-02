# SpydirWebz Website

This is a static website generated from SpydirWebz puzzle files.

## 🚀 Deployment

### GitHub Pages (Recommended)

1. **Create a new repository** on GitHub
2. **Push this website directory** to the repository
3. **Enable GitHub Pages**:
   - Go to repository Settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

Your website will be available at: `https://yourusername.github.io/reponame/`

### Other Static Hosting

This website can be deployed to any static hosting service:
- Netlify
- Vercel
- AWS S3
- Firebase Hosting
- Any web server

## 📁 Files

- `index.html` - Main page with puzzle list
- `puzzle_*.html` - Individual puzzle pages
- `styles.css` - Website styling
- `script.js` - Main JavaScript functionality
- `puzzle-script.js` - Puzzle interaction logic

## 🔄 Updating

To update the website with new puzzles:

1. Run the website generator again:
   ```bash
   python website_generator.py
   ```
2. Push the updated files to your repository
3. GitHub Pages will automatically rebuild

## 🔒 Security

This is a static website with:
- ✅ No server-side code
- ✅ No authentication required
- ✅ No database
- ✅ No user data collection
- ✅ Client-side puzzle validation only

Generated on: 2025-08-02 10:32:09
