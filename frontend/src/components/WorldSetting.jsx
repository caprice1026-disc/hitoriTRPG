import React, { useState } from 'react';
import { TextField, Slider, Typography, Button, Box } from '@mui/material';

function WorldSettingsForm() {
  const [world, setWorld] = useState('');
  const [stage, setStage] = useState('');
  const [chaos, setChaos] = useState(10);

  const handleWorldChange = (event) => {
    setWorld(event.target.value);
  };

  const handleStageChange = (event) => {
    setStage(event.target.value);
  };

  const handleChaosChange = (event, newValue) => {
    setChaos(newValue);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch('/api/worldsettings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ world, stage, chaos })
      });
      const data = await response.json();
      console.log('送信結果:', data);
    } catch (error) {
      console.error('送信エラー:', error);
    }
  };

  return (
    <Box
      component="form"
      noValidate
      autoComplete="off"
      onSubmit={handleSubmit}
      sx={{ maxWidth: 400, mx: 'auto' }}
    >
      <Typography variant="h6" gutterBottom>
        TRPG設定
      </Typography>
      <TextField
        label="世界観"
        multiline
        fullWidth
        rows={4}
        value={world}
        onChange={handleWorldChange}
        margin="normal"
      />
      <TextField
        label="舞台"
        multiline
        fullWidth
        rows={4}
        value={stage}
        onChange={handleStageChange}
        margin="normal"
      />
      <Typography gutterBottom>
        混乱度: {chaos}
      </Typography>
      <Slider
        value={chaos}
        onChange={handleChaosChange}
        aria-labelledby="chaos-slider"
        valueLabelDisplay="auto"
        step={1}
        marks
        min={0}
        max={100}
      />
      <Button type="submit" variant="contained" sx={{ mt: 2 }}>
        送信
      </Button>
    </Box>
  );
}

export default WorldSettingsForm;
