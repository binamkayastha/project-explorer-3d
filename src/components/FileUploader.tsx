
import React, { useCallback } from 'react';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  loading: boolean;
  error: string | null;
}

export const FileUploader: React.FC<FileUploaderProps> = ({
  onFileSelect,
  loading,
  error
}) => {
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    const csvFile = files.find(file => file.name.endsWith('.csv'));
    if (csvFile) {
      onFileSelect(csvFile);
    }
  }, [onFileSelect]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.name.endsWith('.csv')) {
      onFileSelect(file);
    }
  }, [onFileSelect]);

  return (
    <div className="min-h-screen flex items-center justify-center p-8">
      <div className="glass-panel p-12 max-w-2xl w-full text-center space-y-8">
        <div className="space-y-4">
          <h1 className="text-4xl font-bold text-gradient-cosmic">
            IdeaMap
          </h1>
          <p className="text-xl text-muted-foreground">
            Explore, Match, and Save Creative Projects
          </p>
        </div>

        {error && (
          <div className="glass-panel p-4 border-red-500/50 bg-red-500/10 text-red-400 flex items-center gap-3">
            <AlertCircle className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        <div
          className="glass-panel-hover p-12 border-dashed border-2 border-cosmic-aurora/30 transition-all duration-300"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div className="space-y-6">
            <div className="mx-auto w-16 h-16 rounded-full bg-cosmic-aurora/20 flex items-center justify-center">
              {loading ? (
                <div className="cosmic-spinner" />
              ) : (
                <FileText className="w-8 h-8 text-cosmic-aurora" />
              )}
            </div>

            <div className="space-y-2">
              <h3 className="text-xl font-semibold text-foreground">
                Upload Your Project Dataset
              </h3>
              <p className="text-muted-foreground">
                Drop your <code className="px-2 py-1 bg-cosmic-nebula/30 rounded text-cosmic-star">
                  sundai_projects_ready.csv
                </code> file here
              </p>
            </div>

            <div className="space-y-4">
              <Button 
                variant="outline" 
                className="btn-ghost-cosmic"
                onClick={() => document.getElementById('file-input')?.click()}
                disabled={loading}
              >
                <Upload className="w-4 h-4 mr-2" />
                Choose File
              </Button>

              <input
                id="file-input"
                type="file"
                accept=".csv"
                className="hidden"
                onChange={handleFileInput}
              />

              <p className="text-sm text-muted-foreground">
                Expected columns: title, description, tags, category, x, y, z, text, etc.
              </p>
              
              {/* Add detailed format information */}
              <div className="mt-4 p-4 bg-cosmic-nebula/20 rounded-lg text-left">
                <h4 className="font-medium text-foreground mb-2">Required CSV Format:</h4>
                <div className="text-xs space-y-1 text-muted-foreground">
                  <div><strong>Required:</strong> name/title, x/y coordinates (umap_dim_1/umap_dim_2 or x/y)</div>
                  <div><strong>Optional:</strong> z coordinate, description, category, tags, launch_year</div>
                  <div><strong>Example headers:</strong> name, umap_dim_1, umap_dim_2, umap_dim_3, description, category</div>
                  <div><strong>Alternative:</strong> title, x, y, z, detailed_description, category_label</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="text-left space-y-3 text-sm text-muted-foreground">
          <h4 className="text-foreground font-medium">Features:</h4>
          <ul className="space-y-1">
            <li>• 3D Interactive visualization of project ideas</li>
            <li>• AI-powered similarity matching</li>
            <li>• Smart filtering and search</li>
            <li>• Save and export favorite projects</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
