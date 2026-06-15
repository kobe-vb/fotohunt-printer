import { useEffect, useState } from 'react';
import {
  Container,
  Title,
  Button,
  Stack,
  TextInput,
  Card,
  Text,
  Group,
} from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { api } from '../apiClient';

type Team = {
  id: string;
  name: string;
};

export default function HomePage() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [name, setName] = useState('');
  const navigate = useNavigate();

  async function loadTeams() {
    try {
      const data = await api.get<Team[]>('teams');
      setTeams(data);
    } catch (error) {
      console.error('Error loading teams:', error);
      setTeams([]);
    }
  }

  async function createTeam() {
    if (!name.trim()) return;

    const team = await api.post<Team>('teams', { name });

    localStorage.setItem('team_id', team.id);

    navigate('/game');
  }

  function selectTeam(team: Team) {
    localStorage.setItem('team_id', team.id);
    navigate('/game');
  }

  useEffect(() => {
    loadTeams();
  }, []);

  return (
    <Container size="sm" py="xl">
      <Stack gap="md">
        <Title>FotoHunt</Title>

        <Card withBorder>
          <Stack>
            <TextInput
              label="Nieuw team"
              placeholder="Team naam"
              value={name}
              onChange={(e) => setName(e.currentTarget.value)}
            />
            <Button onClick={createTeam}>
              Maak team
            </Button>
          </Stack>
        </Card>

        <Title order={4}>Teams</Title>

        <Stack>
          {teams.map((team) => (
            <Card
              key={team.id}
              withBorder
              onClick={() => selectTeam(team)}
              style={{ cursor: 'pointer' }}
            >
              <Group justify="space-between">
                <Text>{team.name}</Text>
              </Group>
            </Card>
          ))}
        </Stack>
      </Stack>
    </Container>
  );
}