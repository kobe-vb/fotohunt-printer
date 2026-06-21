import { useEffect, useState } from 'react';
import { Container, Title, Stack, Card, Text, TextInput, Button } from '@mantine/core';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../apiClient';

type Team = { id: string; name: string; game_id: string };

export default function JoinPage() {
  const { gameId } = useParams();
  const [teams, setTeams] = useState<Team[]>([]);
  const [name, setName] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    api.get<Team[]>(`games/${gameId}/teams`)
      .then(setTeams)
      .catch(() => setTeams([]));
  }, [gameId]);

  async function createTeam() {
    if (!name.trim()) return;
    await api.post<Team>(`games/${gameId}/teams`, { name });
    localStorage.setItem('team_name', name);
    navigate('/game');
  }

  async function selectTeam(team: Team) {
    
    await api.get(`games/${gameId}/teams/assign/${team.name}`);
    localStorage.setItem('team_name', team.name);
    navigate('/game');
  }

  return (
    <Container size="sm" py="xl">
      <Stack>
        <Title>Kies je team</Title>

        <Card withBorder>
          <Stack>
            <TextInput
              label="Nieuw team"
              placeholder="Team naam"
              value={name}
              onChange={(e) => setName(e.currentTarget.value)}
            />
            <Button onClick={createTeam}>Maak team</Button>
          </Stack>
        </Card>

        <Title order={4}>Of kies een bestaand team</Title>
        {teams.map((team) => (
          <Card
            key={team.id}
            withBorder
            style={{ cursor: 'pointer' }}
            onClick={() => selectTeam(team)}
          >
            <Text>{team.name}</Text>
          </Card>
        ))}
      </Stack>
    </Container>
  );
}