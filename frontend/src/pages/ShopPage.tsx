import { useEffect, useState } from 'react';
import {
  Container,
  Stack,
  Button,
  Text,
  Group,
  Title,
  Tabs,
  Modal,
  Select,
} from '@mantine/core';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { api } from '../apiClient';


type Team = {
  id: string;
  name: string;
  game_id: string;
  sabotage_coins: number;
  shop_coins: number;
  steal_coins: number;
};


const sabotageItems = [
  {
    id: 'blind',
    label: 'Blinddoek (2 rondes)',
  },
  {
    id: 'backwards',
    label: '2 rondes achteruit lopen',
  },
  {
    id: 'half_likes',
    label: '0.5x likes (1 ronde)',
  },
];


const shopItems = [
  {
    id: 'block_steal',
    label: 'Block Steal',
  },
  {
    id: 'extra',
    label: 'Extra kopen',
  },
  {
    id: 'street',
    label: 'Streek kopen',
  },
  {
    id: 'double',
    label: '2x Likes',
  },
];


export default function ShopPage() {
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();

  const [team, setTeam] = useState<Team | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);

  const [tab, setTab] = useState(
    params.get('tab') || 'shop'
  );

  const [confirmOpen, setConfirmOpen] = useState(false);
  const [selectedAction, setSelectedAction] = useState<any>(null);


  async function loadData() {
    const me = await api.get<Team>('teams/me');
    setTeam(me);

    const allTeams = await api.get<Team[]>(`games/${me.game_id}/teams`);
    
    setTeams(
      allTeams.filter(t => t.id !== me.id)
    );
  }

  useEffect(() => {
    loadData();
  }, []);


  function openConfirm(action: any) {
    setSelectedAction(action);
    setConfirmOpen(true);
  }


  async function executeAction() {
    if (!selectedAction || !team) return;

    try {
      if (selectedAction.type === 'sabotage') {
        const me = await api.post<Team>('shop/sabotage', {
          team_id: selectedTeam,
          action: selectedAction.id,
        });
        setTeam(me);
      }


      if (selectedAction.type === 'steal') {
        const me = await api.post<Team>('shop/steal', {
          team_id: selectedTeam,
        });
        setTeam(me);
      }


      if (selectedAction.type === 'buy') {
        const me = await api.post<Team>('shop/buy', {
          item: selectedAction.id,
        });
        setTeam(me);
      }

    } catch (e: any) {
      alert(
        e.message || 'Actie mislukt'
      );
    }
  }


  function changeTab(value: string | null) {
    if (!value) return;

    setTab(value);
    setParams({
      tab: value
    });
  }


  const targetTeams = teams.map(t => ({
    value: t.id,
    label: t.name,
  }));


  if (!team) {
    return (
      <Container py="xl">
        <Text>Laden...</Text>
      </Container>
    );
  }


  return (
    <>
      <Container size="sm" py="md">

        <Group mb="md">
          <Button
            variant="default"
            onClick={() => navigate('/game')}
          >
            ← Terug
          </Button>

          <Title order={3}>
            Shop
          </Title>
        </Group>


        <Tabs
          value={tab}
          onChange={changeTab}
        >
          <Tabs.List>
            <Tabs.Tab value="sabotage">
              Sabotage ({team.sabotage_coins})
            </Tabs.Tab>

            <Tabs.Tab value="shop">
              Shop ({team.shop_coins})
            </Tabs.Tab>

            <Tabs.Tab value="steal">
              Steal ({team.steal_coins})
            </Tabs.Tab>
          </Tabs.List>



          <Tabs.Panel value="sabotage" pt="md">

            <Stack>

              <Select
                label="Doelteam"
                placeholder="Kies team"
                data={targetTeams}
                value={selectedTeam}
                onChange={setSelectedTeam}
              />


              {sabotageItems.map(item => (

                <Button
                  key={item.id}
                  size="lg"
                  disabled={
                    team.sabotage_coins === 0 ||
                    !selectedTeam
                  }
                  onClick={() =>
                    openConfirm({
                      ...item,
                      type: 'sabotage'
                    })
                  }
                >
                  {item.label}
                </Button>

              ))}

            </Stack>

          </Tabs.Panel>




          <Tabs.Panel value="steal" pt="md">

            <Stack>

              <Select
                label="Team"
                placeholder="Kies team"
                data={targetTeams}
                value={selectedTeam}
                onChange={setSelectedTeam}
              />


              <Button
                size="lg"
                disabled={
                  team.steal_coins === 0 ||
                  !selectedTeam
                }
                onClick={() =>
                  openConfirm({
                    id: 'steal',
                    label: 'Steal',
                    type: 'steal'
                  })
                }
              >
                Steal
              </Button>


            </Stack>

          </Tabs.Panel>





          <Tabs.Panel value="shop" pt="md">

            <Stack>

              {shopItems.map(item => (

                <Button
                  key={item.id}
                  size="lg"
                  disabled={
                    team.shop_coins === 0
                  }
                  onClick={() =>
                    openConfirm({
                      ...item,
                      type: 'buy'
                    })
                  }
                >
                  {item.label}
                </Button>

              ))}

            </Stack>

          </Tabs.Panel>


        </Tabs>

      </Container>



      <Modal
        opened={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        title="Bevestigen"
      >

        <Stack>

          <Text>
            Ben je zeker dat je
            {' '}
            <b>
              {selectedAction?.label}
            </b>
            {' '}
            wil uitvoeren?
          </Text>


          <Group justify="end">

            <Button
              variant="default"
              onClick={() => setConfirmOpen(false)}
            >
              Annuleren
            </Button>


            <Button
              onClick={() => {
                setConfirmOpen(false);
                executeAction();
              }}
            >
              Ja
            </Button>

          </Group>

        </Stack>

      </Modal>

    </>
  );
}