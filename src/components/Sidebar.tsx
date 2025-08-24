
import React, { useState } from 'react';
import { Search, Filter, X, Sparkles, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { ProjectFilter } from '@/types/project';

interface SidebarProps {
  filters: ProjectFilter;
  onFilterChange: (key: keyof ProjectFilter, value: any) => void;
  onClearFilters: () => void;
  filterOptions: {
    categories: string[];
    subcategories: string[];
    yearRange: [number, number];
  };
  onAISearch: (query: string) => void;
  aiSearchLoading: boolean;
  projectCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({
  filters,
  onFilterChange,
  onClearFilters,
  filterOptions,
  onAISearch,
  aiSearchLoading,
  projectCount
}) => {
  const [aiQuery, setAiQuery] = useState('');

  const handleAISubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (aiQuery.trim()) {
      onAISearch(aiQuery.trim());
    }
  };

  return (
    <div className="sidebar w-80 min-w-80">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-gradient-cosmic">IdeaMap</h2>
        <p className="text-sm text-muted-foreground">
          {projectCount} projects loaded
        </p>
      </div>

      {/* AI Similarity Search */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cosmic-aurora" />
          <h3 className="font-semibold text-cosmic-aurora">AI Project Matcher</h3>
        </div>
        
        <form onSubmit={handleAISubmit} className="space-y-3">
          <Input
            placeholder="Describe your project idea..."
            value={aiQuery}
            onChange={(e) => setAiQuery(e.target.value)}
            className="cosmic-input"
            disabled={aiSearchLoading}
          />
          <Button 
            type="submit" 
            className="btn-cosmic w-full"
            disabled={!aiQuery.trim() || aiSearchLoading}
          >
            {aiSearchLoading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Finding Similar...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 mr-2" />
                Find Similar Projects
              </>
            )}
          </Button>
        </form>
      </div>

      {/* Filters */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4" />
            <h3 className="font-semibold">Filters</h3>
          </div>
          {(filters.category || filters.subcategory || filters.searchTerm || filters.yearRange) && (
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearFilters}
              className="text-xs text-muted-foreground hover:text-foreground"
            >
              Clear All
            </Button>
          )}
        </div>

        {/* Search */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Search</label>
          <div className="relative">
            <Search className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search projects..."
              value={filters.searchTerm || ''}
              onChange={(e) => onFilterChange('searchTerm', e.target.value || undefined)}
              className="cosmic-input pl-10"
            />
            {filters.searchTerm && (
              <button
                onClick={() => onFilterChange('searchTerm', undefined)}
                className="absolute right-3 top-3 text-muted-foreground hover:text-foreground"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Category */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Category</label>
          <Select
            value={filters.category || "all"}
            onValueChange={(value) => onFilterChange('category', value === "all" ? undefined : value)}
          >
            <SelectTrigger className="cosmic-input">
              <SelectValue placeholder="All categories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All categories</SelectItem>
              {filterOptions.categories.map(category => (
                <SelectItem key={category} value={category}>
                  {category}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Subcategory */}
        <div className="space-y-2">
          <label className="text-sm font-medium">Subcategory</label>
          <Select
            value={filters.subcategory || "all"}
            onValueChange={(value) => onFilterChange('subcategory', value === "all" ? undefined : value)}
          >
            <SelectTrigger className="cosmic-input">
              <SelectValue placeholder="All subcategories" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All subcategories</SelectItem>
              {filterOptions.subcategories.map(subcategory => (
                <SelectItem key={subcategory} value={subcategory}>
                  {subcategory}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Year Range */}
        <div className="space-y-3">
          <label className="text-sm font-medium">Launch Year</label>
          <div className="px-2">
            <Slider
              value={filters.yearRange || filterOptions.yearRange}
              onValueChange={(value) => onFilterChange('yearRange', value as [number, number])}
              min={filterOptions.yearRange[0]}
              max={filterOptions.yearRange[1]}
              step={1}
              className="w-full"
            />
          </div>
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{filters.yearRange?.[0] || filterOptions.yearRange[0]}</span>
            <span>{filters.yearRange?.[1] || filterOptions.yearRange[1]}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
