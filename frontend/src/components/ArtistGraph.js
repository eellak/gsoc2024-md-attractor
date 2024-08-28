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

      const centerArtist = artists[0];
      const centerImageInfo = artistImages.find(img => img.name === centerArtist) || {};

      const nodes = artists.map((artist, index) => {
        const angle = (index / (artists.length - 1)) * 2 * Math.PI;
        const imageInfo = artistImages.find(img => img.name === artist) || {};

        if (index === 0) {
          return {
            id: `artist-${index}`,
            label: artist,
            shape: 'circularImage',
            image: centerImageInfo.imageUrl || defaultImage,
            size: 50, 
            x: centerX,
            y: centerY,
            fixed: true,
          };
        } else {
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
        }
      });

      const edges = artists.slice(1).map((_, index) => ({
        id: `edge-${index}`,
        from: 'artist-0', 
        to: `artist-${index + 1}`,
      }));

      setGraph({ nodes, edges });

      setOptions({
        nodes: {
          shape: 'circularImage',
          borderWidth: 3,
          color: {
            border: '#000000',
            background: '#ffffff',
          },
          font: {
            color: '#000000',
          },
        },
        edges: {
          color: '#e0e0e0',
          width: 1.5,
        },
        physics: false,
      });
    }
  }, [artists, artistImages]);

  return (
    <div style={{ height: '500px' }}>
      {graph && graph.nodes.length > 0 && (
        <Graph
          graph={graph}
          options={options}
          events={{
            select: ({ nodes }) => {
              if (nodes.length > 0) {
                console.log('Selected node:', nodes[0]);
              }
            },
          }}
        />
      )}
    </div>
  );
};

export default ArtistGraph;
