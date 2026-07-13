import { useEffect, useState, useMemo } from 'react';
import {
  Container, Group, Text, Button, Stack, Card, Badge,
  FileInput, Title, Box, SimpleGrid, Paper, SegmentedControl
} from '@mantine/core';
import { useNavigate } from 'react-router-dom';
import { api } from '../apiClient';

type Extra = { text: string; likes: number };

type TaskRecord = {
  id: string;
  sequence_number: number;
  location_text: string;
  location_likes: number;
  pose_text: string;
  pose_likes: number;
  object_text: string;
  object_likes: number;
  extras: Extra[];
};

type Team = {
  id: string;
  name: string;
  sabotage_coins: number;
  shop_coins: number;
  steal_coins: number;
  number_of_extras: number;
  block_steal: boolean;
  multiplier: number;
  blindfold: number;
  backwards: number;
  active_task_id: string | null;
  steal_task_id: string | null;
};

type Modifier = { label: string; type: 'block' | 'multiplier' | 'blindfold' | 'backwards' };

const MODIFIER_COLORS: Record<string, string> = {
  block: 'red',
  multiplier: 'teal',
  blindfold: 'gray',
  backwards: 'grape',
};

export default function GamePage() {
  const navigate = useNavigate();
  const [team, setTeam] = useState<Team | null>(null);
  const [task, setTask] = useState<TaskRecord | null>(null);
  const [stealTask, setStealTask] = useState<TaskRecord | null>(null);
  const [submitTarget, setSubmitTarget] = useState<'own' | 'steal'>('own');

  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreviewUrl, setPhotoPreviewUrl] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const modifiers: Modifier[] = useMemo(() => {
    if (!team) return [];
    const mods: Modifier[] = [];
    if (team.block_steal) mods.push({ label: 'Steal geblokkeerd', type: 'block' });
    if (team.multiplier !== 1) mods.push({ label: `Multiplier x${team.multiplier}`, type: 'multiplier' });
    if (team.blindfold > 0) mods.push({ label: `Blinddoek (${team.blindfold})`, type: 'blindfold' });
    if (team.backwards > 0) mods.push({ label: `Achterstevoren (${team.backwards})`, type: 'backwards' });
    return mods;
  }, [team]);

  async function loadData() {
    try {
      const t = await api.get<Team>('teams/me');
      setTeam(t);

      if (!t.active_task_id) {
        setError('Je hebt momenteel geen actieve taak.');
        return;
      }

      const activeTask = await api.get<TaskRecord>(`task/${t.active_task_id}`);
      setTask(activeTask);

      if (t.steal_task_id) {
        const stolen = await api.get<TaskRecord>(`task/${t.steal_task_id}`);
        setStealTask(stolen);
        setSubmitTarget('steal'); // race, dus dit heeft voorrang
      } else {
        setStealTask(null);
        setSubmitTarget('own');
      }
    } catch (err: any) {
      setError(
        err?.message ||
        'Kan teamgegevens niet laden. Controleer je verbinding.'
      );
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {loadData()}, []);

  // Simpele preview van de gekozen foto, geen verwerking
  useEffect(() => {
    if (!photoFile) { setPhotoPreviewUrl(null); return; }
    const url = URL.createObjectURL(photoFile);
    setPhotoPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [photoFile]);

  async function submitPhoto() {
    const targetTask = submitTarget === 'steal' && stealTask ? stealTask : task;
    if (!photoFile || !targetTask) return;
    setSubmitting(true);

    const formData = new FormData();
    formData.append('photo', photoFile, photoFile.name);
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/api/task/${targetTask.id}/submit`,
        { method: 'POST', body: formData, credentials: 'include' }
      );
      if (!res.ok) {
        throw new Error(await res.text());
      }
      setPhotoFile(null);
    } catch (e: any) {
      alert('Indienen mislukt: ' + e.message);
    } finally {
      setSubmitting(false);
    }

    setTimeout(() => {
      loadData();
    }, 3000);
  }


  if (loading) {
    return (
      <Container size="sm" py="xl">
        <Text>Laden...</Text>
      </Container>
    );
  }

  if (error) {
    return (
      <Container size="sm" py="xl">
        <Card withBorder>
          <Stack>
            <Title order={3}>Fout</Title>
            <Text c="red">{error}</Text>

            <Group>
              <Button onClick={() => window.location.reload()}>
                Opnieuw proberen
              </Button>

              <Button
                variant="default"
                onClick={() => navigate('/')}
              >
                Naar home
              </Button>
            </Group>
          </Stack>
        </Card>
      </Container>
    );
  }

  if (!team || !task) return null;

  return (
    <>
      {/* Sticky topbar */}
      <Box
        style={{
          position: 'sticky', top: 0, zIndex: 100,
          background: 'var(--mantine-color-body)',
          borderBottom: '1px solid var(--mantine-color-default-border)',
          padding: '10px 16px',
        }}
      >
        <Group justify="space-between">
          <Text fw={500}>{team.name}</Text>
          <Group gap="xs">
            <Button
              size="compact-sm" variant="default"
              leftSection={<span style={{ width: 8, height: 8, borderRadius: '50%', background: '#E24B4A', display: 'inline-block' }} />}
              onClick={() => navigate('/shop?tab=sabotage')}
            >
              {team.sabotage_coins}
            </Button>
            <Button
              size="compact-sm" variant="default"
              leftSection={<span style={{ width: 8, height: 8, borderRadius: '50%', background: '#EF9F27', display: 'inline-block' }} />}
              onClick={() => navigate('/shop?tab=shop')}
            >
              {team.shop_coins}
            </Button>
            <Button
              size="compact-sm" variant="default"
              leftSection={<span style={{ width: 8, height: 8, borderRadius: '50%', background: '#1D9E75', display: 'inline-block' }} />}
              onClick={() => navigate('/shop?tab=steal')}
            >
              {team.steal_coins}
            </Button>
          </Group>
        </Group>
      </Box>

      <Container size="sm" py="md">
        <Stack gap="md">

          {/* Actieve modifiers */}
          {modifiers.length > 0 && (
            <Card withBorder>
              <Text size="xs" c="dimmed" tt="uppercase" mb="xs">Actieve modifiers</Text>
              <Group gap="xs">
                {modifiers.map((m, i) => (
                  <Badge key={i} color={MODIFIER_COLORS[m.type]} variant="light">
                    {m.label}
                  </Badge>
                ))}
              </Group>
            </Card>
          )}

          {/* Gestolen taak - race! */}
          {stealTask && (
            <Card withBorder style={{ borderColor: 'var(--mantine-color-red-6)', borderWidth: 2 }}>
              <Group justify="space-between" mb="xs">
                <Text size="xs" c="red" tt="uppercase" fw={700}>Gestolen taak · #{stealTask.sequence_number}</Text>
                <Badge color="red">Race!</Badge>
              </Group>
              <Text size="sm" c="dimmed" mb="sm">
                Deze taak is van een ander team gestolen. Wie 'm het eerst indient, krijgt de punten —
                het verliezende team krijgt niets voor deze taak. Je eigen taak hieronder blijft gewoon staan.
              </Text>
              <SimpleGrid cols={3} spacing="sm" mb="sm">
                <Paper p="sm" withBorder>
                  <Text size="xs" c="dimmed">Locatie</Text>
                  <Text size="sm" fw={500}>{stealTask.location_text}</Text>
                  <Text size="xs" c="dimmed">+{stealTask.location_likes} likes</Text>
                </Paper>
                <Paper p="sm" withBorder>
                  <Text size="xs" c="dimmed">Pose</Text>
                  <Text size="sm" fw={500}>{stealTask.pose_text}</Text>
                  <Text size="xs" c="dimmed">+{stealTask.pose_likes} likes</Text>
                </Paper>
                <Paper p="sm" withBorder>
                  <Text size="xs" c="dimmed">Object</Text>
                  <Text size="sm" fw={500}>{stealTask.object_text}</Text>
                  <Text size="xs" c="dimmed">+{stealTask.object_likes} likes</Text>
                </Paper>
              </SimpleGrid>
              {stealTask.extras.map((ex, i) => (
                <Group key={i} justify="space-between" p="xs"
                  style={{ background: 'var(--mantine-color-red-0)', borderRadius: 8, marginTop: 4 }}>
                  <Text size="sm">{ex.text}</Text>
                  <Text size="xs" c="dimmed">+{ex.likes} likes</Text>
                </Group>
              ))}
            </Card>
          )}

          {/* Taak */}
          <Card withBorder>
            <Text size="xs" c="dimmed" tt="uppercase" mb="sm">Taak #{task.sequence_number}</Text>
            <SimpleGrid cols={3} spacing="sm" mb="sm">
              <Paper p="sm" withBorder>
                <Text size="xs" c="dimmed">Locatie</Text>
                <Text size="sm" fw={500}>{task.location_text}</Text>
                <Text size="xs" c="dimmed">+{task.location_likes} likes</Text>
              </Paper>
              <Paper p="sm" withBorder>
                <Text size="xs" c="dimmed">Pose</Text>
                <Text size="sm" fw={500}>{task.pose_text}</Text>
                <Text size="xs" c="dimmed">+{task.pose_likes} likes</Text>
              </Paper>
              <Paper p="sm" withBorder>
                <Text size="xs" c="dimmed">Object</Text>
                <Text size="sm" fw={500}>{task.object_text}</Text>
                <Text size="xs" c="dimmed">+{task.object_likes} likes</Text>
              </Paper>
            </SimpleGrid>
            {task.extras.map((ex, i) => (
              <Group key={i} justify="space-between" p="xs"
                style={{ background: 'var(--mantine-color-default-hover)', borderRadius: 8, marginTop: 4 }}>
                <Text size="sm">{ex.text}</Text>
                <Text size="xs" c="dimmed">+{ex.likes} likes</Text>
              </Group>
            ))}
          </Card>

          {/* Foto upload + preview */}
          <Card withBorder>
            <Text size="xs" c="dimmed" tt="uppercase" mb="sm">Foto uploaden</Text>

            {stealTask && (
              <SegmentedControl
                fullWidth
                mb="sm"
                value={submitTarget}
                onChange={(v) => setSubmitTarget(v as 'own' | 'steal')}
                data={[
                  { label: `Gestolen taak (#${stealTask.sequence_number})`, value: 'steal' },
                  { label: `Eigen taak (#${task.sequence_number})`, value: 'own' },
                ]}
              />
            )}

            <FileInput
              placeholder="Kies foto of open camera"
              accept="image/*"
              value={photoFile}
              onChange={setPhotoFile}
              leftSection={<span>📷</span>}
            />

            {photoFile && photoPreviewUrl && (
              <Stack gap="sm" mt="md">
                <img
                  src={photoPreviewUrl}
                  alt="Preview"
                  style={{ width: '100%', borderRadius: 8, display: 'block' }}
                />
              </Stack>
            )}
          </Card>

          <Button
            fullWidth size="md"
            disabled={!photoFile || submitting}
            loading={submitting}
            onClick={submitPhoto}
          >
            Indienen{stealTask ? (submitTarget === 'steal' ? ' (gestolen taak)' : ' (eigen taak)') : ''}
          </Button>

        </Stack>
      </Container>
    </>
  );
}