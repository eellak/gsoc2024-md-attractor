import React, { useEffect, useState } from 'react';
import Graph from 'react-graph-vis';

const ArtistGraph = ({ artists, artistImages }) => {
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [options, setOptions] = useState({});

  useEffect(() => {
    if (artists && artists.length > 0 && artistImages && artistImages.length > 0) {
      const defaultImage = 'https://via.placeholder.com/100';
      const radius = 200;
      const centerX = 250;
      const centerY = 250;

      console.log('Artist Images in ArtistGraph:', artistImages);

      const nodes = artists.map((artist, index) => {
        const angle = (index / artists.length) * 2 * Math.PI;
        const imageInfo = artistImages.find(img => img.name === artist) || {};
        return {
          id: `artist-${index}`,
          label: artist,
          shape: 'circularImage',
          image: imageInfo.imageUrl || defaultImage,
          size: 30,
          x: centerX + radius * Math.cos(angle),
          y: centerY + radius * Math.sin(angle),
          fixed: true,
        };
      });

      const edges = [];
      for (let i = 0; i < artists.length - 1; i++) {
        edges.push({
          id: `edge-${i}`,
          from: `artist-${i}`,
          to: `artist-${i + 1}`,
        });
      }

      setGraph({ nodes, edges });

      setOptions({
        nodes: {
          shape: 'circularImage',
          borderWidth: 3,
          size: 30,
          color: {
            border: '#000000',
            background: '#ffffff',
          },
          font: {
            color: '#000000',
          },
        },
        edges: {
          color: '#000000',
        },
        physics: false,
      });
    }
  }, [artists, artistImages]);

  return (
    <div style={{ height: '500px', width: '100%' }}>
      {graph && graph.nodes.length > 0 && (
        <Graph 
          graph={graph} 
          options={options} 
          events={{
            selectNode: (event) => {
              const { nodes } = event;
              console.log('Selected node:', nodes[0]);
            },
          }}
        />
      )}
    </div>
  );
};

export default ArtistGraph;
