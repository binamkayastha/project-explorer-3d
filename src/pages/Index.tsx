 
import React from 'react';
import { FileUploader } from '@/components/FileUploader';
import { MainApp } from '@/components/MainApp';
import { useCSVLoader } from '@/hooks/useCSVLoader';
import Navigation from '@/components/Navigation';

const Index = () => {
  const { projects, loading, error, loadCSV } = useCSVLoader();

  // Show main app if projects are loaded
  if (projects.length > 0) {
    return (
      <>
        <Navigation />
        <MainApp initialProjects={projects} />
      </>
    );
  }

  // Show file uploader
  return (
    <>
      <Navigation />
      <FileUploader
        onFileSelect={loadCSV}
        loading={loading}
        error={error}
      />
    </>
  );
};

export default Index;
