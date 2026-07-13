import { Routes, Route, Navigate } from 'react-router-dom';
import GamesPage from './pages/GamesPage';
import JoinPage from './pages/JoinPage';
import GamePage from './pages/GamePage';
import ShopPage from './pages/ShopPage';
import QrCodePage from './pages/QrCodePage';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<GamesPage />} />
      <Route path="/games/:gameId/join" element={<JoinPage />} />
      <Route path="/game" element={<GamePage />} />
      <Route path="/shop" element={<ShopPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />

      <Route path="/qrcode" element={<QrCodePage />} />
    </Routes>
  );
}