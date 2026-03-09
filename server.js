const express = require('express');
const app = express();

app.use(express.json());

// in-memory store for demonstration purposes
const appointments = new Map();

// Cancel (delete) appointment endpoint as described in KAN-4
app.delete('/appointments/:id', (req, res) => {
  const { id } = req.params;
  if (!appointments.has(id)) {
    // not found
    return res.status(404).json({ error: 'Appointment not found' });
  }
  appointments.delete(id);
  res.json({ message: 'Appointment canceled' });
});

// placeholder for other endpoints

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Appointment service listening on port ${port}`));
