import { useEffect, useState } from 'react';
import { Container, Title, Stack, Card, Text, TextInput, Button } from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { api } from '../apiClient';

type Game = { id: string; name: string; created_at: string };

export default function GamesPage() {
  const [games, setGames] = useState<Game[]>([]);
  const [name, setName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    api.get<Game[]>('games').then(setGames).catch(() => setGames([]));
  }, []);

  async function createGame() {
    if (!name.trim()) return;
    const game = await api.post<Game>('games', { name });
    navigate(`/games/${game.id}/join`);
  }

  return (
    <Container size="sm" py="xl">
      <Stack>
        <Title>Foto Hunt</Title>

        <Card withBorder>
          <Stack>
            <TextInput
              label="Nieuwe game"
              placeholder="Game naam"
              value={name}
              onChange={(e) => setName(e.currentTarget.value)}
            />
            <Button onClick={createGame}>Maak game</Button>
          </Stack>
        </Card>

        <Title order={4}>Of kies een bestaande game</Title>
        {games.map((game) => (
          <Card
            key={game.id}
            withBorder
            style={{ cursor: 'pointer' }}
            onClick={() => navigate(`/games/${game.id}/join`)}
          >
            <Text>{game.name}</Text>
          </Card>
        ))}
      </Stack>
    </Container>
  );
}