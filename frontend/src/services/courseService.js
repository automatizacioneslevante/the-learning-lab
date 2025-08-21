export async function getCoursePreviews() {
    const res = await fetch('/api/v1/catalog/courses_preview/');
    if (!res.ok) {
        throw new Error('Failed to fetch course previews');
    }
    return res.json();
}