// import { Amplify, API, graphqlOperation } from "aws-amplify";
// import { createTodo } from "@/graphql/mutations";
// const awsmobile = {
//     aws_project_region: "ap-southeast-1",
//     aws_appsync_graphqlEndpoint:
//         "https://2isxopc4xfbcvmou7h7syygfyy.appsync-api.ap-southeast-1.amazonaws.com/graphql",
//     aws_appsync_region: "ap-southeast-1",
//     aws_appsync_authenticationType: "API_KEY",
//     aws_appsync_apiKey: "da2-wzyx3ucgobdejap3ulsyn2kb7i",
// };
// Amplify.configure(awsmobile);

// export default async function handler(req, res) {
//     const props = await getServerSideProps();
//     res.status(200).json(props);
// }

// export async function getServerSideProps() {
//     const awsmobile = {
//         aws_project_region: "ap-southeast-1",
//         aws_appsync_graphqlEndpoint:
//             "https://2isxopc4xfbcvmou7h7syygfyy.appsync-api.ap-southeast-1.amazonaws.com/graphql",
//         aws_appsync_region: "ap-southeast-1",
//         aws_appsync_authenticationType: "API_KEY",
//         aws_appsync_apiKey: "da2-wzyx3ucgobdejap3ulsyn2kb7i",
//     };
//     Amplify.configure(awsmobile);
//     const todosData = await API.graphql(graphqlOperation(listTodos));
//     const todosItems = todosData.data.listTodos.items;
//     return todosItems;
// }
