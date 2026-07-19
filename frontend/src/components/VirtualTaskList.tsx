import { useVirtualizer } from "@tanstack/react-virtual";
import { useRef } from "react";
import {
    Badge,
    Card,
    Group,
    Image,
    Paper,
    SimpleGrid,
    Stack,
    Text,
} from "@mantine/core";

type Extra = {
    text: string;
    likes: number;
};

type TaskRecord = {
    id: string;
    sequence_number: number;

    location_text: string | null;
    location_likes: number;

    pose_text: string | null;
    pose_likes: number;

    object_text: string | null;
    object_likes: number;

    special_task_text: string | null;
    special_task_likes: number;

    extras: Extra[];

    photo_url: string | null;
    multiplier: number;
    is_stolen: boolean;
};

function taskLikes(task: TaskRecord) {
    if (task.special_task_text !== null) {
        return task.special_task_likes ?? 0;
    }

    return (
        (task.location_likes ?? 0) +
        (task.pose_likes ?? 0) +
        (task.object_likes ?? 0)
    );
}

export default function VirtualTaskList({
    tasks,
    apiBase,
}: {
    tasks: TaskRecord[];
    apiBase: string;
}) {
    const parentRef = useRef<HTMLDivElement>(null);

    const rowVirtualizer = useVirtualizer({
        count: tasks.length,
        getScrollElement: () => parentRef.current,
        estimateSize: () => 500,
        overscan: 5,
        // belangrijk: laat de virtualizer echt de DOM-hoogte gebruiken,
        // inclusief marges (paddingBottom zit op het gemeten element)
        measureElement: (el) => el.getBoundingClientRect().height,
    });

    return (
        <div
            ref={parentRef}
            style={{
                height: "80vh",
                overflow: "auto",
                contain: "strict",
            }}
        >
            <div
                style={{
                    height: rowVirtualizer.getTotalSize(),
                    position: "relative",
                    width: "100%",
                }}
            >
                {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                    const task = tasks[virtualRow.index];

                    return (
                        <div
                            key={task.id}
                            ref={rowVirtualizer.measureElement}
                            data-index={virtualRow.index}
                            style={{
                                position: "absolute",
                                top: 0,
                                left: 0,
                                width: "100%",
                                transform: `translateY(${virtualRow.start}px)`,
                                paddingBottom: 16,
                            }}
                        >
                            <Card withBorder>
                                <Group justify="space-between">
                                    <Text size="xs">
                                        Taak #{task.sequence_number} x{task.multiplier}
                                    </Text>

                                    <Badge>
                                        {taskLikes(task) * task.multiplier} likes
                                    </Badge>
                                </Group>

                                <Stack mt="md">
                                    {task.photo_url && (
                                        <Image
                                            src={`${apiBase}${task.photo_url}`}
                                            radius="md"
                                            fit="contain"
                                            onLoad={() =>
                                                rowVirtualizer.measureElement(
                                                    document.querySelector(
                                                        `[data-index="${virtualRow.index}"]`
                                                    ) as HTMLElement
                                                )
                                            }
                                        />
                                    )}

                                    {task.special_task_text ? (
                                        <Paper withBorder p="sm">
                                            <Text size="xs">Opdracht</Text>
                                            <Text>
                                                {task.special_task_text} (
                                                {task.special_task_likes * task.multiplier})
                                            </Text>
                                        </Paper>
                                    ) : (
                                        <SimpleGrid cols={3}>
                                            <Paper withBorder p="sm">
                                                <Text size="xs">Locatie</Text>
                                                <Text>
                                                    {task.location_text} (
                                                    {task.location_likes * task.multiplier})
                                                </Text>
                                            </Paper>

                                            <Paper withBorder p="sm">
                                                <Text size="xs">Pose</Text>
                                                <Text>
                                                    {task.pose_text} (
                                                    {task.pose_likes * task.multiplier})
                                                </Text>
                                            </Paper>

                                            <Paper withBorder p="sm">
                                                <Text size="xs">Object</Text>
                                                <Text>
                                                    {task.object_text} (
                                                    {task.object_likes * task.multiplier})
                                                </Text>
                                            </Paper>
                                        </SimpleGrid>
                                    )}

                                    {task.extras.map((extra, i) => (
                                        <Text key={i} size="sm">
                                            {extra.text} ({extra.likes * task.multiplier})
                                        </Text>
                                    ))}
                                </Stack>
                            </Card>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}