export const fetchArtistImages = async (artistIds) => {
  try {
    const clientId = process.env.REACT_APP_SPOTIFY_CLIENT_ID;
    const clientSecret = process.env.REACT_APP_SPOTIFY_CLIENT_SECRET;

    if (!clientId || !clientSecret) {
      return artistIds.map(id => ({ id, imageUrl: null, error: "Client ID or Client Secret not set" }));
    }

    const asciiString = `${clientId}:${clientSecret}`;

    const headers = {
      "Authorization": 'Basic ' + btoa(asciiString),
      "Content-Type": "application/x-www-form-urlencoded",
    };

    const tokenResponse = await fetch("https://accounts.spotify.com/api/token", {
      method: "POST",
      headers,
      body: "grant_type=client_credentials",
    });

    if (!tokenResponse.ok) {
      throw new Error(`Token request failed: ${tokenResponse.statusText}`);
    }

    const tokenData = await tokenResponse.json();
    const accessToken = tokenData.access_token;

    const artistPromises = artistIds.map(async (artistId) => {
      const artistResponse = await fetch(`https://api.spotify.com/v1/artists/${artistId}`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (!artistResponse.ok) {
        return { id: artistId, imageUrl: null, error: artistResponse.statusText };
      }

      const artistData = await artistResponse.json();
      const imageUrl = artistData.images[0]?.url || null;
      return { id: artistId, imageUrl, name: artistData.name };
    });

    const artistImages = await Promise.all(artistPromises);
    return artistImages;
  } catch (error) {
    return artistIds.map(id => ({ id, imageUrl: null, error: error.message }));
  }
};
