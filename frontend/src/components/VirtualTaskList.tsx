import { useVirtualizer } from "@tanstack/react-virtual";
import { useRef } from "react";

import {
    Card,
    Text,
    Stack,
    Group,
    Badge,
    Image,
    SimpleGrid,
    Paper
} from "@mantine/core";


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

};



export default function VirtualTaskList({

    tasks,
    apiBase

}: {

    tasks: TaskRecord[];

    apiBase: string;

}) {


    const parentRef =
        useRef<HTMLDivElement>(null);



    const virtualizer =
        useVirtualizer({

            count: tasks.length,

            getScrollElement:
                () => parentRef.current,

            estimateSize:
                () => 350

        });



    return (

        <div

            ref={parentRef}

            style={{
                height: 800,
                overflow: "auto"
            }}

        >


            <div

                style={{

                    height:
                        virtualizer.getTotalSize(),

                    position: "relative"

                }}

            >


                {
                    virtualizer
                        .getVirtualItems()
                        .map(item => {


                            const task =
                                tasks[item.index];


                            return (

                                <div

                                    key={task.id}

                                    style={{

                                        position: "absolute",

                                        top: 0,

                                        left: 0,

                                        width: "100%",

                                        transform:
                                            `translateY(${item.start}px)`

                                    }}

                                >


                                    <Card withBorder>


                                        <Group justify="space-between">

                                            <Text size="xs">
                                                Taak #{task.sequence_number}
                                            </Text>


                                            <Badge>
                                                {task.location_likes +
                                                    task.pose_likes +
                                                    task.object_likes}
                                                likes
                                            </Badge>


                                        </Group>



                                        <Stack mt="md">


                                            {
                                                task.photo_url && (

                                                    <Image

                                                        src={`${apiBase}${task.photo_url}`}

                                                        mah={300}

                                                        radius="md"

                                                    />

                                                )

                                            }



                                            <SimpleGrid cols={3}>


                                                <Paper p="sm" withBorder>

                                                    <Text size="xs">
                                                        Locatie
                                                    </Text>

                                                    <Text>
                                                        {task.location_text}
                                                    </Text>

                                                </Paper>



                                                <Paper p="sm" withBorder>

                                                    <Text size="xs">
                                                        Pose
                                                    </Text>

                                                    <Text>
                                                        {task.pose_text}
                                                    </Text>

                                                </Paper>



                                                <Paper p="sm" withBorder>

                                                    <Text size="xs">
                                                        Object
                                                    </Text>

                                                    <Text>
                                                        {task.object_text}
                                                    </Text>

                                                </Paper>


                                            </SimpleGrid>



                                            {
                                                task.extras.map((extra, i) => (

                                                    <Text key={i} size="sm">

                                                        {extra.text}
                                                        +{extra.likes}
                                                    </Text>
                                                ))
                                            }
                                        </Stack>
                                    </Card>
                                </div>
                            )
                        })
                }
            </div>
        </div>
    )
}