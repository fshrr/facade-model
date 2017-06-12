addpath /home/work/Projects/workstudy/facade-model/deep-photo-styletransfer/gen_laplacian/matting/
addpath /home/work/Projects/workstudy/facade-model/deep-photo-styletransfer/gen_laplacian/gaimc/

# list for the id of input images
id_list = [4]

pkg load image


for id_list_index = 1:numel(id_list)
    i = id_list(id_list_index)
    prefix = '../trials/input/';
    in_name = [prefix 'in' int2str(i) '.png'];
    disp(['Working on image index = ' int2str(i)]);

    input = im2double(imread(in_name));
    input = reshape_img(input, 700);
    size(input)

    close all
    figure; imshow(input);

    [h w c] = size(input);

    disp('Compute Laplacian');
    A = getLaplacian1(input, zeros(h, w), 1e-7, 1);


    disp('Save to disk');
    n = nnz(A);
    [Ai, Aj, Aval] = find(A);
    CSC = [Ai, Aj, Aval];
    %save(['./generated/Input_Laplacian_3x3_1e-7_CSC' int2str(i) '.mat'], 'CSC');

    [rp ci ai] = sparse_to_csr(A);
    Ai = sort(Ai);
    Aj = ci;
    Aval = ai;
    CSR = [Ai, Aj, Aval];
    save(['./generated/Input_Laplacian_3x3_1e-7_CSR' int2str(i) '.mat'], 'CSR');

    # processing the output to generate into mat7-binary file that matio can open in th
		data = load(['./generated/Input_Laplacian_3x3_1e-7_CSR' int2str(i) '.mat']);
    out_file = strcat('./generated/Input_Laplacian_3x3_1e-7_CSR', int2str(i), '.mat')
    save('-mat7-binary', out_file, 'data');
end
