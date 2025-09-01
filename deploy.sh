#!/bin/bash

echo "🚀 Deploying Sundai AI Explorer to Vercel..."

# Build the project
echo "📦 Building project..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    # Deploy to Vercel
    echo "🌐 Deploying to Vercel..."
    vercel --prod
    
    echo "🎉 Deployment complete!"
    echo "🌍 Your app is now live on Vercel!"
else
    echo "❌ Build failed. Please check the errors above."
    exit 1
fi
