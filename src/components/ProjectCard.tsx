
import React from 'react';
import { ExternalLink, Github, Calendar, Users, Tag } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Project } from '@/types/project';

interface ProjectCardProps {
  project: Project;
  onClose?: () => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({ project, onClose }) => {
  const tags = project.tags.split(',').map(tag => tag.trim()).filter(Boolean);

  return (
    <div className="project-card animate-scale-in">
      <div className="space-y-4">
        {/* Header */}
        <div className="space-y-2">
          <h3 className="text-xl font-bold text-gradient-star line-clamp-2">
            {project.title}
          </h3>
          <div className="text-sm text-cosmic-aurora font-medium">
            {project.category_label}
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-muted-foreground line-clamp-3">
          {project.description}
        </p>

        {/* Tags */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {tags.slice(0, 3).map((tag, index) => (
              <span key={index} className="project-tag">
                {tag}
              </span>
            ))}
            {tags.length > 3 && (
              <span className="project-tag">
                +{tags.length - 3}
              </span>
            )}
          </div>
        )}

        {/* Metadata */}
        <div className="space-y-2 text-xs text-muted-foreground">
          {project.launch_year && (
            <div className="flex items-center gap-2">
              <Calendar className="w-3 h-3" />
              <span>{project.launch_year}</span>
            </div>
          )}
          
          {project.team && (
            <div className="flex items-center gap-2">
              <Users className="w-3 h-3" />
              <span className="truncate">{project.team}</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          {project.project_url && (
            <Button
              size="sm"
              variant="outline"
              className="btn-ghost-cosmic flex-1"
              onClick={(e) => {
                e.stopPropagation();
                window.open(project.project_url, '_blank');
              }}
            >
              <ExternalLink className="w-3 h-3 mr-1" />
              Visit
            </Button>
          )}
          
          {project.github_url && (
            <Button
              size="sm"
              variant="outline"
              className="btn-ghost-cosmic flex-1"
              onClick={(e) => {
                e.stopPropagation();
                window.open(project.github_url, '_blank');
              }}
            >
              <Github className="w-3 h-3 mr-1" />
              Code
            </Button>
          )}
        </div>

        {onClose && (
          <Button
            size="sm"
            variant="ghost"
            className="w-full mt-2 text-muted-foreground hover:text-foreground"
            onClick={onClose}
          >
            Close
          </Button>
        )}
      </div>
    </div>
  );
};
