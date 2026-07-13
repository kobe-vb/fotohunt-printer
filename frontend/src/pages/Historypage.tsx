import { useEffect, useState } from "react";
import {
    Container,
    Title,
    Stack,
    Text,
    Group,
    Badge,
    Accordion,
    Button,
} from "@mantine/core";

import { useNavigate, useParams } from "react-router-dom";
import { api } from "../apiClient";
import VirtualTaskList from "../components/VirtualTaskList";


type Extra = {
    text: string;
    likes: number;
};


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

    photo_url: string | null;

    submitted_at?: string | null;
};


type Team = {
    id: string;
    name: string;
    task_count: number;
};


type TaskPageResponse = {
    items: TaskRecord[];
    next_offset: number | null;
};


const API_BASE = import.meta.env.VITE_API_URL;


export default function HistoryPage() {

    const { gameId } = useParams();

    const navigate = useNavigate();


    const [teams, setTeams] = useState<Team[]>([]);

    const [tasks, setTasks] = useState<
        Record<string, TaskRecord[]>
    >({});


    const [offsets, setOffsets] = useState<
        Record<string, number | null>
    >({});


    const [loading, setLoading] = useState(true);


    useEffect(() => {

        if (!gameId)
            return;


        api.get<Team[]>(
            `games/${gameId}/teams`
        )
        .then(setTeams)
        .finally(() => setLoading(false));


    }, [gameId]);



    async function loadTasks(teamId: string) {

        const offset =
            offsets[teamId] ?? 0;


        const result =
            await api.get<TaskPageResponse>(
                `games/${gameId}/teams/history?offset=${offset}&limit=50`
            );


        setTasks(prev => ({
            ...prev,
            [teamId]: [
                ...(prev[teamId] ?? []),
                ...result.items
            ]
        }));


        setOffsets(prev => ({
            ...prev,
            [teamId]: result.next_offset
        }));
    }



    if (loading) {

        return (
            <Container py="xl">
                <Text>Laden...</Text>
            </Container>
        );
    }



    return (

        <Container size="md" py="xl">

            <Stack gap="xl">


                <Group justify="space-between">

                    <Title order={2}>
                        Geschiedenis
                    </Title>


                    <Button
                        variant="default"
                        onClick={() => navigate("/")}
                    >
                        ← Terug
                    </Button>

                </Group>



                {
                teams.length === 0 && (

                    <Text c="dimmed">
                        Nog geen teams.
                    </Text>

                )
                }



                <Accordion
                    variant="separated"

                    onChange={(opened)=>{

                        if (!opened)
                            return;

                        if(opened.length === 0)
                            return;


                        const teamId =
                            opened[opened.length - 1];


                        if(!tasks[teamId]) {
                            loadTasks(teamId);
                        }

                    }}
                >


                {
                teams.map(team => (

                    <Accordion.Item
                        key={team.id}
                        value={team.id}
                    >


                        <Accordion.Control>

                            <Group justify="space-between">

                                <Text fw={600}>
                                    {team.name}
                                </Text>


                                <Badge>
                                    {team.task_count} taken
                                </Badge>

                            </Group>

                        </Accordion.Control>



                        <Accordion.Panel>


                            <Stack gap="md">


                                {
                                tasks[team.id] && (

                                    <VirtualTaskList
                                        tasks={tasks[team.id]}
                                        apiBase={API_BASE}
                                    />

                                )
                                }



                                <Button

                                    disabled={
                                        offsets[team.id] === null
                                    }

                                    onClick={() =>
                                        loadTasks(team.id)
                                    }

                                >
                                    {
                                    offsets[team.id] === null
                                    ?
                                    "Alles geladen"
                                    :
                                    "Meer laden"
                                    }

                                </Button>


                            </Stack>


                        </Accordion.Panel>


                    </Accordion.Item>

                ))
                }


                </Accordion>


            </Stack>


        </Container>

    );
}